import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from slack_alert import slack_alert_fn


#  This allows imports from 'etl' directory
sys.path.append('/opt/airflow/etl')

from extract.log_generator import write_fake_logs
from transform.session_transformer import transform_logs
from load.load_to_postgres import load_logs_to_postgres

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'depends_on_past': False,
    'on_failure_callback': slack_alert_fn,
}


with DAG(
    dag_id='log_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for simulated SaaS logs',
    start_date=datetime(2025, 5, 22),
    schedule_interval='@daily',
    catchup=False,
    tags=['etl'],
) as dag:

    extract_task = PythonOperator(
        task_id='extract_logs',
        python_callable=write_fake_logs,
        op_kwargs={
            'output_dir': '/opt/airflow/data/raw_logs',
            'execution_date': '{{ ds }}'  # Airflow renders this as 'YYYY-MM-DD'
        }
    )

    transform_task = PythonOperator(
        task_id='transform_logs',
        python_callable=transform_logs,
        op_kwargs={
            'input_dir': '/opt/airflow/data/raw_logs',
            'output_dir': '/opt/airflow/data/processed_logs',
            'execution_date': '{{ ds }}'
        },
        dag=dag,
    )

    load_task = PythonOperator(
        task_id='load_logs_to_postgres',
        python_callable=load_logs_to_postgres,
        op_kwargs={
            'output_dir': '/opt/airflow/data/processed_logs',
            'execution_date': '{{ ds }}'
        },
        dag=dag,
    )

    # Task dependencies
    extract_task >> transform_task >> load_task
