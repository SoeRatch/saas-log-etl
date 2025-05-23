import json
import os
from datetime import datetime, timezone
import random

import logging
from common.logging_config import configure_logging
from common.file_utils import get_raw_log_path

configure_logging()


def write_fake_logs(output_dir: str, execution_date: str):

    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create output directory '{output_dir}': {e}")
        return

    filepath = get_raw_log_path(output_dir, execution_date)

    event_types = ['login', 'logout', 'click', 'view', 'purchase']
    users = [f"user_{i}" for i in range(1, 21)]

    try:
        with open(filepath, "w") as f:
            for _ in range(10):  # generate 10 fake events
                try:
                    log = {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "user_id": random.choice(users),
                        "event": random.choice(event_types),
                        "session_id": f"session_{random.randint(1000, 9999)}"
                    }
                    f.write(json.dumps(log) + "\n")
                except Exception as e:
                    logging.warning(f"Skipping a log due to error: {e}")
    except Exception as e:
        logging.error(f"Failed to write log file at '{filepath}': {e}")
        return
    
    logging.info(f"Wrote logs to {filepath}")
