import os
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


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

    # Read raw logs
    try:
        with open(input_file, "r") as infile:
            raw_logs = [json.loads(line) for line in infile]
        logging.info(f"Read {len(raw_logs)} logs from {input_file}")
    except FileNotFoundError:
        logging.error(f"Input file not found: {input_file}")
        return
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in file {input_file}: {e}")
        return
    except Exception as e:
        logging.error(f"Unexpected error while reading {input_file}: {e}")
        return
    

    # Transform logs
    transformed = []
    for log in raw_logs:
        try:
            transformed.append({
                "timestamp": log.get("timestamp"),
                "level": map_event_to_level(log.get("event")),
                "message": generate_message(log),
                "user_id": log.get("user_id"),
                "session_id": log.get("session_id"),
            })
        except Exception as e:
            logging.warning(f"Skipping transform of log due to error: {e}")
            continue

    # Write transformed logs
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, "w") as outfile:
            for t in transformed:
                outfile.write(json.dumps(t) + "\n")
        
        logging.info(f"Transformed logs written to {output_file}")
    except Exception as e:
        logging.error(f"Failed to write transformed logs to {output_file}: {e}")
    
