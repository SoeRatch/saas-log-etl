import os
import json
import tempfile
from unittest.mock import patch
from etl.transform.session_transformer import transform_logs

def test_transform_logs():
    with tempfile.TemporaryDirectory() as raw_dir, tempfile.TemporaryDirectory() as processed_dir:
        execution_date = "2025-05-23"
        input_path = os.path.join(raw_dir, f"raw_{execution_date}.jsonl")
        output_path = os.path.join(processed_dir, f"processed_{execution_date}.jsonl")

        # Create a raw log file with one event
        raw_log = {
            "timestamp": "2025-05-23T12:00:00Z",
            "user_id": "user_1",
            "event": "login",
            "session_id": "session_1234"
        }

        with open(input_path, "w") as f:
            f.write(json.dumps(raw_log) + "\n")

        # Patch the file_utils functions to use temp paths
        with patch("etl.transform.session_transformer.get_raw_log_path", return_value=input_path), \
             patch("etl.transform.session_transformer.get_processed_log_path", return_value=output_path):
            # Run the transform
            transform_logs(raw_dir, processed_dir, execution_date)


        # check if the output file was created
        assert os.path.exists(output_path)

        with open(output_path, "r") as f:
            lines = f.readlines()
            assert len(lines) == 1
            transformed = json.loads(lines[0])
            assert transformed["user_id"] == "user_1"
            assert transformed["level"] == "info"
            assert transformed["message"] == "User user_1 logged in"