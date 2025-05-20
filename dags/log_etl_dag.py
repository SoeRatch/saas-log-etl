# dags/log_etl_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Let Airflow find our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from extract.generator import write_logs

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="saas_log_etl",
    default_args=default_args,
    description="ETL pipeline for SaaS app logs",
    start_date=datetime(2025, 5, 20),
    schedule_interval="@hourly",  # change to "@daily" if needed
    catchup=False
) as dag:

    generate_logs = PythonOperator(
        task_id="generate_logs",
        python_callable=write_logs,
        op_kwargs={"num_entries": 100}
    )

    # Dummy stubs for now — real ones in next steps
    def transform_logs():
        print("Transforming logs...")

    def load_data_to_db():
        print("Loading data to database...")

    transform_task = PythonOperator(
        task_id="transform_logs",
        python_callable=transform_logs
    )

    load_task = PythonOperator(
        task_id="load_to_db",
        python_callable=load_data_to_db
    )

    generate_logs >> transform_task >> load_task
