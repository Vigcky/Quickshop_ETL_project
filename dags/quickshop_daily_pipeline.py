from airflow.decorators import dag, task
from datetime import datetime, timedelta
import subprocess, shlex, psycopg2, json

@dag(
    dag_id="quickshop_daily_pipeline",
    start_date=datetime(2025, 11, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "email_on_failure": True,
        "email": ["alerts@quickshop.local"],
    },
    tags=["quickshop", "etl"],
)
def quickshop_daily_pipeline():

    @task
    def run_etl(ds: str):
        cmd = (
            f"python /opt/airflow/run_etl.py "
            f"--input-dir /opt/airflow/data "
            f"--output-dir /opt/airflow/out "
            f"--start-date {ds} --end-date {ds} "
            f"--format db "
            f"--db-url postgresql+psycopg2://postgres:182003@postgres:5432/quickshop"
        )
        subprocess.check_call(shlex.split(cmd))
        return f"ETL completed for {ds}"

    @task
    def generate_daily_report(ds: str):
        conn = psycopg2.connect(
            host="postgres", dbname="quickshop", user="postgres", password="182003"
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT SUM(order_total) AS daily_revenue
            FROM orders_transformed
            WHERE order_date = %s;
        """, (ds,))
        revenue = cur.fetchone()[0] or 0
        cur.close()
        conn.close()

        report = {"date": ds, "daily_revenue": float(revenue)}
        with open(f"/opt/airflow/out/report_{ds}.json", "w") as f:
            json.dump(report, f)
        return report

    etl_task = run_etl("{{ ds }}")
    report_task = generate_daily_report("{{ ds }}")

    etl_task >> report_task

quickshop_daily_pipeline()
