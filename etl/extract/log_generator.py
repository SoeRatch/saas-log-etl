import json
import os
from datetime import datetime, timezone
import random

def write_fake_logs():
    log_dir = "/opt/airflow/data/raw_logs"
    os.makedirs(log_dir, exist_ok=True)

    filename = f"log_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.jsonl"
    filepath = os.path.join(log_dir, filename)

    event_types = ['login', 'logout', 'click', 'view', 'purchase']
    users = [f"user_{i}" for i in range(1, 21)]

    with open(filepath, "w") as f:
        for _ in range(100):  # generate 100 fake events
            log = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "user_id": random.choice(users),
                "event": random.choice(event_types),
                "session_id": f"session_{random.randint(1000, 9999)}"
            }
            f.write(json.dumps(log) + "\n")

    print(f"Wrote logs to {filepath}")
