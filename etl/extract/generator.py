# extract/generator.py

import os
import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
LOG_DIR = "extract/raw_logs"

EVENT_TYPES = ["login", "logout", "search", "view", "download", "error"]

def generate_log_entry():
    return {
        "user_id": fake.uuid4(),
        "event_type": random.choice(EVENT_TYPES),
        "timestamp": datetime.utcnow().isoformat(),
        "ip_address": fake.ipv4(),
        "user_agent": fake.user_agent(),
        "session_id": fake.uuid4()
    }

def write_logs(num_entries=100, file_prefix="logs"):
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{file_prefix}_{timestamp}.json"
    filepath = os.path.join(LOG_DIR, filename)

    logs = [generate_log_entry() for _ in range(num_entries)]
    with open(filepath, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"Wrote {num_entries} log entries to {filepath}")

if __name__ == "__main__":
    write_logs()
