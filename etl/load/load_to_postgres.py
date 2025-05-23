import os
import json
import psycopg2
from psycopg2.extras import execute_values
import logging
logging.basicConfig(level=logging.INFO)

def load_logs_to_postgres(output_dir, execution_date):
    filename = f"processed_{execution_date}.jsonl"
    file_path = os.path.join(output_dir, filename)

    logging.info(f"Looking for file at: {file_path}")

    if not os.path.exists(file_path):
        logging.info(f"No processed log file found at {file_path}")
        return

    with open(file_path, "r") as f:
        logs = [json.loads(line) for line in f if line.strip()]

    if not logs:
        logging.info("No logs to load.")
        return

    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            dbname="airflow",
            user="airflow",
            password="airflow",
            host="postgres",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_logs (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ,
                level VARCHAR(20),
                message TEXT,
                user_id VARCHAR(50),
                session_id VARCHAR(50)
            )
        """)

        values = [
            (
                log["timestamp"],
                log["level"],
                log["message"],
                log["user_id"],
                log["session_id"]
            )
            for log in logs
        ]

        insert_query = """
            INSERT INTO processed_logs (timestamp, level, message, user_id, session_id)
            VALUES %s
        """

        try:
            execute_values(cursor, insert_query, values)
            conn.commit()
            logging.info(f"Loaded {len(values)} log records into PostgreSQL.")
        except Exception as e:
            logging.info(f"Error loading to PostgreSQL: {e}")

    except Exception as e:
        logging.info(f"Error during loading logs: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
