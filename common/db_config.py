import os

def get_db_config():
    return {
        "dbname": os.getenv("DB_NAME", "airflow"),
        "user": os.getenv("DB_USER", "airflow"),
        "password": os.getenv("DB_PASSWORD", "airflow"),
        "host": os.getenv("DB_HOST", "postgres"),
        "port": os.getenv("DB_PORT", "5432"),
    }
