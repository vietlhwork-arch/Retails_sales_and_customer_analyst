# AdventureWorks Analytics

A complete end-to-end analytics project for the AdventureWorks retail dataset:
data ingestion, cleaning, feature engineering, EDA, modeling, SQL preparation, and a Streamlit dashboard.

## Project goals

- Build a clean analytical layer from the raw CSV files.
- Produce a unified `master_sales.csv` for BI and ML use cases.
- Explore customer, product, territory, and return behavior.
- Train baseline models for segmentation or prediction tasks.
- Provide a lightweight Streamlit app for interactive analysis.

## Suggested dataset layout

Place the CSV files you downloaded into `data/raw/`:

- Calendar Lookup.csv
- Customer Lookup.csv
- Product Lookup.csv
- Product Category Lookup.csv
- Product Subcategory Lookup.csv
- Territory Lookup.csv
- Returns Data.csv
- Sales Data 2020.csv
- Sales Data 2021.csv
- Sales Data 2022.csv

The exact filenames can vary a little; the loader tries to match by keywords.

## Main outputs

- `data/processed/master_sales.csv`
- `data/processed/customer_summary.csv`
- `data/processed/product_summary.csv`
- `data/processed/territory_summary.csv`
- `reports/eda_report.html`
- `reports/model_metrics.json`
- `dashboards/README.md` for Power BI guidance

## How to run

### 1) Create a virtual environment

```bash
python -m venv .venv
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run preprocessing

```bash
python -m src.data_preprocessing --raw-dir data/raw --out-dir data/processed
```

### 4) Run modeling

```bash
python -m src.model_training --input data/processed/master_sales.csv --out reports
```

### 5) Launch the app

```bash
streamlit run app/streamlit_app.py
```

## Folder purpose

- `data/raw/`: original source CSV files
- `data/processed/`: cleaned and merged analytical tables
- `sql_scripts/`: SQL extraction and transformation queries
- `notebooks/`: analysis notebooks
- `src/`: reusable Python code
- `dashboards/`: Power BI notes and DAX placeholders
- `app/`: Streamlit app

## Notes

This project is designed so you can swap in the real Kaggle files without changing the code.
If you later build a `.pbix`, place it under `dashboards/`.
