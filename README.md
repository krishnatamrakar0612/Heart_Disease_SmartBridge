# Heart Disease Analysis

End-to-end heart disease analytics project using Python, PostgreSQL, SQL, Tableau, and a simple Flask web interface.

## Overview

This project analyzes heart disease risk patterns from a public health dataset. It includes:

- Data cleaning and feature standardization in Python
- PostgreSQL data loading with indexing for faster query performance
- SQL query pack for analysis and dashboard-ready aggregations
- Tableau Story and Dashboard workbooks
- Flask web page to present Tableau embeds

## Tech Stack

- Python (`pandas`, `numpy`, `psycopg2`, `python-dotenv`, `flask`)
- PostgreSQL
- SQL
- Tableau
- Flask + HTML/CSS

## Project Structure

```text
Heart Disease analysis/
├── data/
│   ├── Heart_disease_raw.csv
│   └── Heart_disease_cleaned.csv
├── scripts/
│   ├── clean_data.py
│   └── load_data.py
├── sql/
│   ├── analysis_queries.sql
│   └── queries_refrence.md
├── heart_disease_web/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── Static/
│       ├── css/main.css
│       ├── js/main.js
│       ├── img/
│       └── vendor/
├── tableau/
│   └── workbooks/
├── Dashboard/
├── Story/
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Data Pipeline

### 1. Clean raw data

Script: `scripts/clean_data.py`

Main operations:

- Standardize column names
- Remove duplicates
- Handle missing numeric values (median) and categorical values (mode)
- Clip BMI outliers using IQR bounds
- Simplify diabetic categories
- Fix data types
- Encode binary categorical features (Yes/No to 1/0 for selected columns)

Output:

- `data/Heart_disease_cleaned.csv`

Run:

```bash
python scripts/clean_data.py
```

### 2. Load cleaned data into PostgreSQL

Script: `scripts/load_data.py`

What it does:

- Reads cleaned CSV
- Creates table `heart_disease`
- Inserts all rows in batch
- Creates indexes on key analysis columns
- Prints verification summary

Required `.env` file in project root:

```env
PGDATABASE=heart_disease_db
PGUSER=postgres
PGPASSWORD=your_password
PGHOST=localhost
PGPORT=5432
```

Run:

```bash
python scripts/load_data.py
```

## SQL Analysis

Use `sql/analysis_queries.sql` for analysis and Tableau dataset preparation.

Includes queries for:

- Table overview and quality checks
- Gender vs heart disease
- Age vs heart disease
- Diabetes vs stroke
- Smoking/alcohol impact
- Stroke vs co-morbid conditions
- Race-wise distribution
- General health vs heart disease
- Physical activity vs heart disease
- BMI and age segmentation

Reference notes and chart mapping are documented in:

- `sql/queries_refrence.md`

## Web App (Flask)

Location: `heart_disease_web/`

The web app serves a static analysis page with embedded Tableau Story and Dashboard.

Run:

```bash
cd heart_disease_web
python app.py
```

Then open:

- `http://127.0.0.1:5000/`

## Setup

You can run this project using either `uv` or standard `pip`.

### Option A: Using uv

```bash
uv sync
```

Run scripts with:

```bash
uv run scripts/clean_data.py
uv run scripts/load_data.py
cd heart_disease_web
uv run app.py
```

### Option B: Using pip

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## End-to-End Workflow

1. Place raw dataset in `data/Heart_disease_raw.csv`
2. Run `scripts/clean_data.py`
3. Configure PostgreSQL credentials in `.env`
4. Run `scripts/load_data.py`
5. Execute SQL queries from `sql/analysis_queries.sql`
6. Open Tableau workbooks for dashboarding
7. Launch Flask app from `heart_disease_web/app.py`

## Notes

- `pyproject.toml` currently specifies `requires-python = ">=3.14"`.
- If your local Python version is lower, update this constraint to your target runtime.
- File naming in the project uses `Static/` (capital `S`) inside `heart_disease_web`.

## Author

Heart Disease Analysis Project
