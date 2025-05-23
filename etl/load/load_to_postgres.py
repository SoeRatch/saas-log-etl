import os
import json
import psycopg2
from psycopg2.extras import execute_values
from common.db_config import get_db_config

import logging
from common.logging_config import configure_logging
from common.file_utils import get_processed_log_path

configure_logging()


def load_logs_to_postgres(output_dir, execution_date):
    file_path = get_processed_log_path(output_dir, execution_date)

    logging.info(f"Looking for file at: {file_path}")

    if not os.path.exists(file_path):
        logging.warning(f"No processed log file found at {file_path}")
        return

    # Read transformed logs
    try:
        with open(file_path, "r") as f:
            logs = [json.loads(line) for line in f if line.strip()]
        logging.info(f"Loaded {len(logs)} logs from {file_path}")
    except Exception as e:
        logging.error(f"Failed to read or parse JSON logs: {e}")
        return


    if not logs:
        logging.info("No logs to load.")
        return

    # Database operation
    conn = None
    cursor = None
    try:
        # Database connection
        conn = psycopg2.connect(**get_db_config())
        cursor = conn.cursor()


        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_logs (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ,
                level VARCHAR(20),
                message TEXT,
                user_id VARCHAR(50),
                session_id VARCHAR(50),
                created_at TIMESTAMPTZ DEFAULT NOW(),
                CONSTRAINT uniq_log_event UNIQUE (timestamp, user_id, session_id)
            )
        """)

        # Prepare values
        try:
            values = [
                (
                    log["timestamp"],
                    log["level"],
                    log["message"],
                    log["user_id"],
                    log["session_id"]
                ) for log in logs
            ]
        except KeyError as e:
            logging.error(f"Missing expected log field: {e}")
            return

        #  If a row already exists with the same (timestamp, user_id, session_id), it will update the level and message fields.
        insert_query = """
            INSERT INTO processed_logs (timestamp, level, message, user_id, session_id)
            VALUES %s
            ON CONFLICT (timestamp, user_id, session_id) DO UPDATE
            SET 
                level = EXCLUDED.level,
                message = EXCLUDED.message
        """

        # Bulk insert
        try:
            execute_values(cursor, insert_query, values)
            conn.commit()
            logging.info(f"Loaded {len(values)} log records into PostgreSQL.")
        except Exception as e:
            conn.rollback()
            logging.error("Error inserting records into PostgreSQL: %s", e)

    except Exception as e:
        logging.error("Error during database operations: %s", e)
        if conn:
            conn.rollback()
    finally:
        # Safe cleanup
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except Exception as e:
            logging.warning(f"Error closing DB connection: {e}")
