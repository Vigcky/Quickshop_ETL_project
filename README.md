# 🏪 Quickshop ETL Project  

End-to-end **ETL (Extract–Transform–Load)** data pipeline for **QuickShop**, featuring:  
✅ Data ingestion from CSV  
✅ Schema validation & transformation  
✅ PostgreSQL persistence  
✅ Flask REST API  
✅ Apache Airflow orchestration  
✅ SQL analytics queries  
✅ Full Dockerized environment  

---

## 🚀 Overview  

This project simulates a real-world **data engineering workflow** for an online retail platform.  
The pipeline reads raw CSV data (orders, products, inventory), applies schema validation & transformation, and writes processed data to a PostgreSQL database or Parquet files.  

Airflow then orchestrates this ETL daily, while Flask provides API endpoints for managing and querying data.  

---

## ⚙️ Features  

| Component | Description |
|------------|--------------|
| 🧩 **Python ETL** | Reads CSVs, validates schema, transforms orders (e.g. `order_total = qty * unit_price`) |
| 🧱 **Schema Validation** | Implemented using `pydantic` models |
| 💾 **PostgreSQL** | Stores transformed data |
| 🔄 **Airflow DAG** | Automates daily ETL & summary generation |
| 🌐 **Flask REST API** | CRUD endpoints for orders (`/orders`) |
| 🧮 **SQL Scripts** | Analytical queries for revenue, performance, cohorts |
| 🧪 **Pytest** | Unit-tested extract, transform, load components |
| 🐳 **Docker Compose** | Orchestrates Flask, Airflow, and PostgreSQL containers |

---

## 🏗️ Architecture  

               ┌──────────────────────────┐
               │        CSV Input          │
               │  (orders, products, inv)  │
               └────────────┬──────────────┘
                            │
                    [Extract: Pandas]
                            │
                    [Transform: Pydantic]
                            │
                    [Load: PostgreSQL/Parquet]
                            │
       ┌────────────────────┴────────────────────┐
       │                                         │
            [Airflow DAGs] [Flask API Layer]
       │                                         │
        [Automates Daily ETL] [CRUD + Reporting]
       │                                         │
       └────────────────────┬────────────────────┘
                            │
                [SQL Analytical Reports]


---

## 🧩 Project Structure  

Quickshop_ETL_Project/
├── Quickshop_ETL/
│ ├── extract.py
│ ├── transform.py
│ ├── load.py
│ ├── schema.py
│ ├── analytics.py
│ └── init.py
│
├── dags/
│ └── quickshop_daily_pipeline.py
│
├── sql/
│ ├── daily_revenue.sql
│ ├── product_performance.sql
│ ├── inventory_alerts.sql
│ └── cohort_retention.sql
│
├── data/
│ ├── products.csv
│ ├── inventory.csv
│ └── orders_20251101.csv
│
├── tests/
│ ├── test_extract.py
│ ├── test_transform.py
│ ├── test_load.py
│ └── conftest.py
│
├── run_etl.py
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── init.sql
└── README.md

---

## ⚡ Setup Options  

### 🧱 Option 1 — Manual Setup (Recommended for testing)  

1️⃣ **Install dependencies**  
```bash
uv sync
or with pip:
    pip install -r requirements.txt
2️⃣ **Create PostgreSQL database manually**
psql -U postgres
CREATE DATABASE quickshop;
\c quickshop
\i init.sql
3️⃣ Run ETL manually:
python run_etl.py --input-dir data --output-dir out \
  --start-date 2025-11-01 --end-date 2025-11-05 \
  --format db \
  --db-url postgresql+psycopg2://postgres:182003@localhost:5432/quickshop

🐳 Option 2 — Docker Compose (All-in-one)
     docker-compose up --build

Then access:

Flask API → http://localhost:5000/orders

Airflow UI → http://localhost:8080
 (login: admin / admin)

PostgreSQL → localhost:5432 (user: postgres, pass: 182003)


💾 Flask API Endpoints
| Method | Endpoint  | Description     |
| ------ | --------- | --------------- |
| GET    | `/orders` | List all orders |
| POST   | `/orders` | Add new order   |
| GET    | `/health` | Health check    |



⏱️ Airflow Orchestration

DAG Name: quickshop_daily_pipeline

Schedule: Daily (@daily)

Tasks:

Extract data from /data

Transform and validate

Load into PostgreSQL

Generate summary JSON report

File: dags/quickshop_daily_pipeline.py


📊 SQL Analytical Queries

| File                      | Purpose                                 |
| ------------------------- | --------------------------------------- |
| `daily_revenue.sql`       | Computes daily revenue & top categories |
| `product_performance.sql` | Tracks units sold & return rates        |
| `inventory_alerts.sql`    | Finds low-stock products                |
| `cohort_retention.sql`    | Cohort retention trends                 |


🧪 Testing

Run all unit tests:

pytest -v
