from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Iterable, Optional

import numpy as np
import pandas as pd

# 1. Tối ưu lại RAW_FILE_PATTERNS để sử dụng đúng
RAW_FILE_PATTERNS = {
    "calendar": ["calendar"],
    "customer": ["customer"],
    "subcategory": ["product subcategories", "subcategories"],
    "category": ["product categories", "categories"],
    "product": ["product lookup", "product"],
    "territory": ["territory"],
    "returns": ["returns"],
    "sales_2020": ["sales data 2020"],
    "sales_2021": ["sales data 2021"],
    "sales_2022": ["sales data 2022"],
}

def _normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip().lower()

def find_files(raw_dir: Path) -> Dict[str, Path]:
    files = {}
    for path in raw_dir.iterdir():
        if not path.is_file() or path.suffix.lower() != ".csv":
            continue
            
        name = path.name.lower()
        # Duyệt qua từ điển để tự động gán file đúng nhãn
        for key, patterns in RAW_FILE_PATTERNS.items():
            if any(p in name for p in patterns) and key not in files:
                files[key] = path
                break

    required = list(RAW_FILE_PATTERNS.keys())
    missing = [k for k in required if k not in files]

    if missing:
        raise FileNotFoundError(f"Could not find required CSV files for: {missing}")

    return files

def load_csv(path: Path) -> pd.DataFrame:
    encodings = ["utf-8", "cp1252", "latin1", "ISO-8859-1"]
    last_error = None
    for enc in encodings:
        try:
            print(f"Loading {path.name} with encoding={enc}")
            return pd.read_csv(path, encoding=enc)
        except Exception as e:
            last_error = e
    raise last_error

def safe_rename(df: pd.DataFrame) -> pd.DataFrame:
    cols = {}
    for c in df.columns:
        clean = re.sub(r"[^0-9a-zA-Z]+", "_", str(c)).strip("_").lower()
        cols[c] = clean
    return df.rename(columns=cols)

def parse_dates(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce")
    return out

def cast_keys_to_int(df: pd.DataFrame, keys: Iterable[str]) -> pd.DataFrame:
    """Hàm chuẩn hóa khóa Key sang số nguyên (hỗ trợ NaN) để Merge không bị lỗi"""
    out = df.copy()
    for col in keys:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").astype("Int64")
    return out

def build_master_sales(
    sales: pd.DataFrame,
    product: pd.DataFrame,
    customer: pd.DataFrame,
    territory: pd.DataFrame,
    category: Optional[pd.DataFrame] = None,
    subcategory: Optional[pd.DataFrame] = None,
    calendar: Optional[pd.DataFrame] = None,
    returns: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    
    # Chuẩn hóa tên cột
    sales = safe_rename(sales)
    product = safe_rename(product)
    customer = safe_rename(customer)
    territory = safe_rename(territory)
    if category is not None: category = safe_rename(category)
    if subcategory is not None: subcategory = safe_rename(subcategory)
    if calendar is not None: calendar = safe_rename(calendar)
    if returns is not None: returns = safe_rename(returns)

    # Chuẩn hóa Ngày tháng
    sales = parse_dates(sales, ["orderdate", "stockdate", "order_date", "stock_date"])
    customer = parse_dates(customer, ["birthdate"])
    if calendar is not None: calendar = parse_dates(calendar, ["date"])
    if returns is not None: returns = parse_dates(returns, ["returndate", "return_date"])

    # Chuẩn hóa các Khóa Merge (Tránh lỗi chuỗi "1.0" != "1")
    key_columns = ["productkey", "customerkey", "territorykey", "salesterritorykey", "productsubcategorykey", "productcategorykey"]
    sales = cast_keys_to_int(sales, key_columns)
    product = cast_keys_to_int(product, key_columns)
    customer = cast_keys_to_int(customer, key_columns)
    territory = cast_keys_to_int(territory, key_columns)
    if category is not None: category = cast_keys_to_int(category, key_columns)
    if subcategory is not None: subcategory = cast_keys_to_int(subcategory, key_columns)
    if returns is not None: returns = cast_keys_to_int(returns, key_columns)

    # Tiến hành Merge Data (Mô hình Star Schema vào bảng Fact)
    merged = sales.merge(product, how="left", on="productkey", suffixes=("", "_product"))
    merged = merged.merge(customer, how="left", on="customerkey", suffixes=("", "_customer"))
    merged = merged.merge(territory, how="left", left_on="territorykey", right_on="salesterritorykey", suffixes=("", "_territory"))

    if subcategory is not None and "productsubcategorykey" in merged.columns:
        merged = merged.merge(subcategory, how="left", on="productsubcategorykey", suffixes=("", "_subcategory"))

    if category is not None and "productcategorykey" in merged.columns:
        merged = merged.merge(category, how="left", on="productcategorykey", suffixes=("", "_category"))

    if calendar is not None and "orderdate" in merged.columns and "date" in calendar.columns:
        cal = calendar.rename(columns={"date": "orderdate"})
        merged = merged.merge(cal, how="left", on="orderdate", suffixes=("", "_calendar"))

    # Ép kiểu dữ liệu để tính toán Doanh thu, Lợi nhuận
    if "orderquantity" in merged.columns:
        merged["orderquantity"] = pd.to_numeric(merged["orderquantity"], errors="coerce").fillna(0)
    if "productprice" in merged.columns:
        merged["productprice"] = pd.to_numeric(merged["productprice"], errors="coerce")
    if "productcost" in merged.columns:
        merged["productcost"] = pd.to_numeric(merged["productcost"], errors="coerce")

    merged["revenue"] = merged["orderquantity"] * merged.get("productprice", np.nan)
    merged["cost"] = merged["orderquantity"] * merged.get("productcost", np.nan)
    merged["profit"] = merged["revenue"] - merged["cost"]

    # Phân tách thời gian
    if "orderdate" in merged.columns:
        merged["order_year"] = merged["orderdate"].dt.year
        merged["order_month"] = merged["orderdate"].dt.to_period("M").astype(str)
        merged["order_quarter"] = merged["orderdate"].dt.to_period("Q").astype(str)

    # Tính độ tuổi khách hàng
    if "birthdate" in merged.columns:
        today = pd.Timestamp.today().normalize()
        merged["age"] = (today - merged["birthdate"]).dt.days // 365

    return merged

def summarize_table(df: pd.DataFrame, key: str, metric_col: str, top_n: int = 20) -> pd.DataFrame:
    if key not in df.columns or metric_col not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby(key, dropna=False, as_index=False)[metric_col]
        .sum()
        .sort_values(metric_col, ascending=False)
        .head(top_n)
    )

def load_dataset_bundle(raw_dir: Path):
    files = find_files(raw_dir)
    return {name: load_csv(path) for name, path in files.items()}

def main(raw_dir: str, out_dir: str) -> None:
    raw_path = Path(raw_dir)
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    data = load_dataset_bundle(raw_path)

    # Ghép 3 file Sales lại với nhau
    master_sales_raw = pd.concat([data["sales_2020"], data["sales_2021"], data["sales_2022"]], ignore_index=True, sort=False)

    master = build_master_sales(
        sales=master_sales_raw,
        product=data["product"],
        customer=data["customer"],
        territory=data["territory"],
        category=data["category"],
        subcategory=data["subcategory"],
        calendar=data["calendar"],
        returns=data["returns"],
    )

    master.to_csv(out_path / "master_sales.csv", index=False)

    # Tính toán bảng tóm tắt
    customer_summary = summarize_table(master, "customerkey", "revenue")
    product_summary = summarize_table(master, "productkey", "revenue")
    territory_summary = summarize_table(master, "territorykey", "revenue")

    customer_summary.to_csv(out_path / "customer_summary.csv", index=False)
    product_summary.to_csv(out_path / "product_summary.csv", index=False)
    territory_summary.to_csv(out_path / "territory_summary.csv", index=False)

    meta = {
        "rows_master": int(master.shape[0]),
        "cols_master": int(master.shape[1]),
        "columns": list(master.columns),
    }
    (out_path / "metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n✅ Đã lưu Master Table thành công tại: {out_path / 'master_sales.csv'}")
    print(f"📊 Dữ liệu có {master.shape[0]:,} dòng | {master.shape[1]:,} cột")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default="data/raw")
    parser.add_argument("--out-dir", default="data/processed")
    args = parser.parse_args()
    
    # Để tránh lỗi khi chạy script trực tiếp trên Jupyter/Colab bằng sys.argv
    try:
        main(args.raw_dir, args.out_dir)
    except SystemExit:
        main("data/raw", "data/processed")