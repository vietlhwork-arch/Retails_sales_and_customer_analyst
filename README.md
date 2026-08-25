# 🛒 End-to-End Retail Sales & Customer Analytics (AdventureWorks)

Đây là dự án phân tích dữ liệu bán lẻ toàn diện (End-to-End) dựa trên tập dữ liệu AdventureWorks. Dự án mô phỏng một bài toán doanh nghiệp thực tế, đi từ khâu xây dựng Data Pipeline tự động (ETL), ứng dụng Học máy (Machine Learning) để tìm kiếm insight, cho đến thiết kế Data Model và trực quan hóa dữ liệu qua **Power BI** và **Streamlit**.

Dự án không chỉ dừng lại ở mức độ báo cáo (Reporting) mà còn hướng tới **Hỗ trợ ra quyết định (Decision Support)** thông qua các phân tích dự báo rủi ro và mô phỏng giá bán (What-If Analysis).

---

## 🌟 Key Highlights & AI Insights

Thông qua việc kết hợp AI vào phân tích Business Intelligence, dự án đã bóc tách được những Insight kinh doanh mang tính chiến lược (Xem chi tiết tại `KeyInsight.pdf`):

- 🎯 **Phân cụm khách hàng bằng AI (K-Means):** Tự động phân chia khách hàng dựa trên mô hình RFM. Kết quả cho thấy nhóm **"Khách hàng Tiềm năng"** là động lực tăng trưởng cốt lõi, đóng góp áp đảo **65.03% (~$16M)** tổng doanh thu.
- ⚠️ **Quản trị rủi ro chủ động (XGBoost):** Dự báo sớm xác suất trả hàng, phát hiện mảng "Bikes" có doanh thu rủi ro lớn nhất (>$20M). Đặc biệt, cảnh báo các dòng lốp xe (Mountain/Road) có xác suất trả hàng lên tới 99% để yêu cầu QA/QC rà soát khẩn cấp.
- 💡 **Mô phỏng kịch bản kinh doanh (What-If Pricing):** Đánh giá trực tiếp tác động của việc thay đổi giá bán đến biên lợi nhuận, hỗ trợ chiến lược định giá (Pricing Strategy) thay vì tăng giá cảm tính.
- 🌍 **Thị trường trọng điểm:** Europe là khu vực đóng góp doanh thu lớn nhất, trong khi Pacific mang lại tiềm năng tăng trưởng cao. Khách hàng VIP tiêu biểu (như Mr. Maurice Shan - $12.4K) được định vị để đưa vào Loyalty Program.

---

## 📂 Cấu trúc dự án (Project Structure)

```text
AdventureWorks_Analytics/
├── Project_BI.pbix             # [NEW] File Power BI hoàn chỉnh (Constellation Schema, DAX, Dashboards)
├── KeyInsight.pdf              # [NEW] Slide thuyết trình tổng hợp Insights & Business Recommendations
├── app/
│   └── streamlit_app.py        # Web App tương tác viết bằng Streamlit
├── dashboards/                 # Tài liệu hướng dẫn thiết kế Dashboard
├── data/
│   ├── raw/                    # Dữ liệu CSV gốc (Sales 2020-2022, Customer, Product,...)
│   └── processed/              # Dữ liệu đã qua làm sạch và xử lý (ETL)
├── notebooks/                  # Jupyter notebooks cho quá trình phân tích EDA & ML experiments
├── reports/                    # Các file dữ liệu xuất ra sau khi chạy Model (KMeans)
├── sql_scripts/                # Các truy vấn SQL trích xuất/biến đổi dữ liệu mẫu
├── src/                        
│   ├── data_preprocessing.py   # Script Python tự động hóa Data Pipeline (ETL)
│   └── model_training.py       # Script Python huấn luyện mô hình Machine Learning
├── dax_measures.md             # Tổng hợp các hàm DAX (Time Intelligence, Target, Filter...)
├── requirements.txt            # Danh sách thư viện Python
└── README.md
```

---

## 📊 Power BI Dashboards (`Project_BI.pbix`)

Hệ thống Dashboard được thiết kế chuẩn chỉnh với mô hình **Constellation Schema**, cung cấp 5 góc nhìn toàn diện cho các cấp quản lý:

1. **Executive Summary:** Tổng hợp điều hành, tích hợp AI Insights (Customer Segments & Risk Alerts).
2. **Sales Performance:** Theo dõi hiệu quả kinh doanh tổng thể (Revenue, Profit, Target Gap, Return Rate).
3. **Customer Analytics:** Phân tích hành vi, giá trị vòng đời khách hàng và Loyalty Tracking.
4. **Product Analytics:** Đánh giá hiệu suất sản phẩm, kết hợp *What-if Pricing* để tối ưu lợi nhuận.
5. **Geographic Analytics:** Phân tích hiệu quả kinh doanh qua Map Visualization theo từng khu vực.

---

## 🛠️ Technology Stack

- **Data Engineering & ETL:** Python (Pandas, Numpy)
- **Machine Learning / AI:** Scikit-learn (K-Means Clustering), XGBoost (Predictive Modeling)
- **Business Intelligence & Data Modeling:** Power BI (DAX, Constellation Schema)
- **Interactive Web App:** Streamlit
- **Database / Querying:** SQL

---

## 🚀 Hướng dẫn chạy dự án (How to run)

### 1. Cài đặt môi trường (Windows PowerShell)

Mở Terminal tại thư mục gốc của dự án và chạy:

```powershell
# Tạo và kích hoạt môi trường ảo
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Cài đặt thư viện
pip install -r requirements.txt
```
*(Nếu PowerShell báo lỗi không cho chạy script, dùng lệnh: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### 2. Chạy Data Pipeline (Xử lý dữ liệu)

```powershell
python -m src.data_preprocessing --raw-dir data/raw --out-dir data/processed
```
*Lưu ý: Bạn cần đặt đủ các file CSV gốc vào thư mục `data/raw/` trước khi chạy.*

### 3. Huấn luyện mô hình phân cụm (K-Means)

```powershell
python -m src.model_training --input data/processed/master_sales.csv --out reports
```

### 4. Khởi chạy Streamlit Dashboard Web App

```powershell
streamlit run app/streamlit_app.py
```

### 5. Xem báo cáo Power BI
Chỉ cần mở file **`Project_BI.pbix`** bằng phần mềm Power BI Desktop để trải nghiệm toàn bộ Data Model, các hàm DAX nâng cao và các trang Dashboard tương tác.
