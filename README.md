# 🚀 QuickShop ETL Project  

End-to-end **ETL (Extract–Transform–Load)** pipeline for **QuickShop**, featuring:  
✅ Automated data ingestion from CSV  
✅ Schema validation & transformation  
✅ PostgreSQL persistence  
✅ Flask REST API  
✅ Apache Airflow orchestration  
✅ SQL analytics & reports  
✅ Fully Dockerized setup  

---

## 🧭 Overview  

This project simulates a production-grade **data engineering workflow** for an e-commerce platform.  
The pipeline extracts raw order, product, and inventory data from CSVs, validates and transforms it, and loads it into a PostgreSQL database or Parquet files.  

**Apache Airflow** automates daily ETL execution, and a **Flask API** provides CRUD and analytics endpoints.  

---

## 🧩 Features  

| Component | Description |
|------------|-------------|
| **Python ETL** | Reads CSVs, validates schema, and transforms data (e.g. `order_total = qty * unit_price`) |
| **Schema Validation** | Uses `pydantic` for strong type checking |
| **PostgreSQL Database** | Stores processed orders, products, and inventory |
| **Airflow DAG** | Orchestrates daily ETL and reporting workflows |
| **Flask REST API** | CRUD endpoints for managing and querying orders |
| **SQL Analytics** | Predefined queries for revenue, performance, and retention |
| **Unit Tests (pytest)** | Tests for extract, transform, and load modules |
| **Docker Compose** | Spins up Flask, Airflow, and PostgreSQL containers easily |

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
   │     [Airflow DAGs]      [Flask API]     │
   │   (Daily Automation)   (CRUD + Query)   │
   └────────────────────┬────────────────────┘
                        │
             [SQL Analytical Reports]


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
   │     [Airflow DAGs]      [Flask API]     │
   │   (Daily Automation)   (CRUD + Query)   │
   └────────────────────┬────────────────────┘
                        │
             [SQL Analytical Reports]




## 📂 Project Structure  

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

## ⚙️ Setup Options  

### 🧪 Option 1 — Manual Setup (Recommended for Local Testing)

#### 1. Install dependencies  

uv sync
# or with pip
pip install -r requirements.txt

**2. Create PostgreSQL database**

psql -U postgres
CREATE DATABASE quickshop;
\c quickshop
\i init.sql

**Option 2 — Docker Compose (All-in-One)**

docker-compose up --build

**Flask API Endpoints**
| Method | Endpoint  | Description           |
| ------ | --------- | --------------------- |
| GET    | `/orders` | List all orders       |
| POST   | `/orders` | Add new order         |
| GET    | `/health` | Health check endpoint |

**Airflow Orchestration**

DAG Name: quickshop_daily_pipeline
Schedule: Daily (@daily)

Tasks:

Extract data from /data

Transform and validate

Load into PostgreSQL

Generate summary JSON report

File: dags/quickshop_daily_pipeline.py


**SQL Analytical Queries**
| File                      | Purpose                                           |
| ------------------------- | ------------------------------------------------- |
| `daily_revenue.sql`       | Computes daily revenue and top product categories |
| `product_performance.sql` | Tracks units sold, returns, and profit margin     |
| `inventory_alerts.sql`    | Flags low-stock or out-of-stock products          |
| `cohort_retention.sql`    | Analyzes user retention by order cohorts          |



**Testing**

Run all unit tests using pytest:

🧪 Testing

Run all unit tests using pytest:
pytest -v
Tests include:

test_extract.py → CSV ingestion & schema validation

test_transform.py → Business logic (e.g., totals, conversions)

test_load.py → Database & Parquet writes

**Tech Stack:**
| Category          | Technology              |
| ----------------- | ----------------------- |
| **Language**      | Python 3.10+            |
| **Validation**    | Pydantic                |
| **Database**      | PostgreSQL              |
| **Orchestration** | Apache Airflow          |
| **API Framework** | Flask                   |
| **Testing**       | Pytest                  |
| **Packaging**     | Docker & Docker Compose |
| **Analytics**     | SQL                     |



