import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# 👇 This allows imports from your 'etl' directory
sys.path.append('/opt/airflow/etl')

from extract.log_generator import write_fake_logs
from transform.session_transformer import transform_logs
from load.load_to_postgres import load_to_postgres

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='log_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for simulated SaaS logs',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id='extract_logs',
        python_callable=write_fake_logs
    )

    transform_task = PythonOperator(
        task_id='transform_logs',
        python_callable=transform_logs
    )

    load_task = PythonOperator(
        task_id='load_to_db',
        python_callable=load_to_postgres
    )

    extract_task >> transform_task >> load_task
