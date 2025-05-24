import os
import json
import tempfile
import pytest
from unittest import mock
from etl.load.load_to_postgres import load_logs_to_postgres

@mock.patch("etl.load.load_to_postgres.psycopg2.connect")
@mock.patch("etl.load.load_to_postgres.get_processed_log_path")
@mock.patch("etl.load.load_to_postgres.filter_valid_logs")
def test_load_logs_to_postgres(mock_filter_valid_logs, mock_get_path, mock_connect):
    execution_date = "2025-05-23"
    
    # Create temp processed log file
    with tempfile.TemporaryDirectory() as temp_dir:
        log = {
            "timestamp": "2025-05-23T12:00:00Z",
            "level": "info",
            "message": "User user_1 logged in",
            "user_id": "user_1",
            "session_id": "session_1234"
        }

        file_path = os.path.join(temp_dir, f"processed_{execution_date}.jsonl")
        with open(file_path, "w") as f:
            f.write(json.dumps(log) + "\n")
        
        # Patch file_utils.get_processed_log_path
        mock_get_path.return_value = file_path

        # Patch validation_utils.filter_valid_logs
        mock_filter_valid_logs.return_value = ([log], [])

        # Create a mock DB connection
        mock_cursor = mock.MagicMock()
        mock_conn = mock.MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Call the loader
        load_logs_to_postgres(temp_dir, execution_date)

        # Assert: file was read and logs were inserted
        assert mock_cursor.execute.call_count >= 2  # One for CREATE TABLE, one for ETL metadata insert
        assert mock_conn.commit.called

        # Assert that execute_values was called:
        from psycopg2.extras import execute_values
        with mock.patch("etl.load.load_to_postgres.execute_values") as mock_execute_values:
            load_logs_to_postgres(temp_dir, execution_date)
            mock_execute_values.assert_called()
