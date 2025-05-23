import os
import json
import tempfile
from datetime import datetime

from etl.extract.log_generator import write_fake_logs
from common.file_utils import get_raw_log_path


def test_write_fake_logs_creates_file_and_logs():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        execution_date = datetime.now().strftime("%Y-%m-%d")
        log_path = get_raw_log_path(tmpdir, execution_date)

        # Act
        write_fake_logs(tmpdir, execution_date)

        # Assert file exists
        assert os.path.exists(log_path), f"Expected log file not found: {log_path}"

        # Read logs
        with open(log_path, "r") as f:
            lines = f.readlines()

        assert len(lines) == 10, f"Expected 10 log lines, got {len(lines)}"

        # Check format and required keys
        for line in lines:
            log = json.loads(line)
            assert "timestamp" in log
            assert "user_id" in log
            assert "event" in log
            assert "session_id" in log
