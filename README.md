# Quickshop ETL Project

End-to-end ETL, Flask API, and Airflow orchestration pipeline for QuickShop data analytics.

## Features
- Python ETL: CSV ingestion → transformation → PostgreSQL
- Flask REST API: CRUD endpoints for orders
- Apache Airflow DAG: Automated daily ETL & metric calculation
- SQL Analytical Scripts for insights
- Dockerized environment for easy setup

## Tech Stack
- **Python 3.10**
- **Flask**
- **Pandas**
- **PostgreSQL**
- **SQLAlchemy**
- **Apache Airflow**
- **Docker Compose**

## Setup Instructions

```bash
# 1. Build containers
docker-compose up --build

# 2. Check services
# Flask → http://localhost:5000/health
# Airflow → http://localhost:8080 (admin / admin)
# Postgres → localhost:5432 (postgres / 182003)
