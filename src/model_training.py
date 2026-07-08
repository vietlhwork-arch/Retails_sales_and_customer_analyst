from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_input(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def build_feature_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    cols = [c for c in ["revenue", "cost", "profit", "orderquantity", "productprice", "productcost", "age", "return_rate"] if c in out.columns]
    if not cols:
        raise ValueError("No usable numeric columns found for modeling.")
    out = out[cols + [c for c in ["gender", "maritalstatus", "occupation", "country", "continent", "categoryname"] if c in out.columns]]
    return out


def train_kmeans(df: pd.DataFrame, n_clusters: int = 4):
    X = build_feature_frame(df)

    numeric_cols = [c for c in X.columns if pd.api.types.is_numeric_dtype(X[c])]
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    preprocess = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_cols),
            ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                              ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), categorical_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)

    pipe = Pipeline([
        ("preprocess", preprocess),
        ("model", model),
    ])

    labels = pipe.fit_predict(X)
    score = silhouette_score(pipe.named_steps["preprocess"].transform(X), labels) if len(set(labels)) > 1 and len(X) > n_clusters else np.nan

    return pipe, labels, score, X


def main(input_path: str, out_dir: str) -> None:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    df = load_input(Path(input_path))
    pipe, labels, score, X = train_kmeans(df)

    result = X.copy()
    result["cluster"] = labels
    result.to_csv(out_path / "clustered_customers_or_sales.csv", index=False)
    joblib.dump(pipe, out_path / "kmeans_pipeline.joblib")

    metrics = {
        "model": "KMeans",
        "n_clusters": int(pipe.named_steps["model"].n_clusters),
        "silhouette_score": None if pd.isna(score) else float(score),
        "rows_used": int(X.shape[0]),
        "features_used": list(X.columns),
    }
    (out_path / "model_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/processed/master_sales.csv")
    parser.add_argument("--out", default="reports")
    args = parser.parse_args()
    main(args.input, args.out)
