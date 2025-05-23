import os

def get_raw_log_path(output_dir, execution_date):
    # filename = f"log_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.jsonl"
    return os.path.join(output_dir, f"log_{execution_date}.jsonl")

def get_processed_log_path(output_dir, execution_date):
    return os.path.join(output_dir, f"processed_{execution_date}.jsonl")
