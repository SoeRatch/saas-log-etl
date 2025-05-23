# common/validation_utils.py

import logging

REQUIRED_LOG_FIELDS = ["timestamp", "level", "message", "user_id", "session_id"]

def filter_valid_logs(logs):
    valid_logs = []
    invalid_logs = []

    for log in logs:
        if all(key in log for key in REQUIRED_LOG_FIELDS):
            valid_logs.append(log)
        else:
            invalid_logs.append(log)
            logging.warning(f"Skipping invalid log: {log}")

    return valid_logs, invalid_logs
