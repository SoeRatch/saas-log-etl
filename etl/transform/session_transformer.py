# etl/transform/session_transformer.py

import os
import json

def map_event_to_level(event):
    if event in ["logout", "login"]:
        return "info"
    elif event == "purchase":
        return "critical"
    elif event == "view":
        return "debug"
    else:
        return "info"

def generate_message(log):
    event = log.get("event")
    user = log.get("user_id")
    if event == "login":
        return f"User {user} logged in"
    elif event == "logout":
        return f"User {user} logged out"
    elif event == "purchase":
        return f"User {user} made a purchase"
    elif event == "view":
        return f"User {user} viewed a page"
    else:
        return f"User {user} performed {event}"


def transform_logs(input_dir, output_dir, execution_date: str):
    input_file = os.path.join(input_dir, f"log_{execution_date}.jsonl")
    output_file = os.path.join(output_dir, f"processed_{execution_date}.jsonl")

    with open(input_file, "r") as infile:
        raw_logs = [json.loads(line) for line in infile]

    transformed = []

    for log in raw_logs:
        transformed.append({
            "timestamp": log.get("timestamp"),
            "level": map_event_to_level(log.get("event")),
            "message": generate_message(log),
            "user_id": log.get("user_id"),
            "session_id": log.get("session_id"),
        })
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as outfile:
        for t in transformed:
            outfile.write(json.dumps(t) + "\n")
    
    print(f"Transformed logs written to {output_file}")
