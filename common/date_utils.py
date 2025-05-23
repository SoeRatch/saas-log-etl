from datetime import timedelta

def get_time_scope_filter_range(execution_date, granularity="daily"):
    dt = execution_date  # execution_date needs to be a datetime

    if granularity == "hourly":
        start = dt.replace(minute=0, second=0, microsecond=0)
        end = start + timedelta(hours=1)

    elif granularity == "weekly":
        start = dt - timedelta(days=dt.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=7)
        
    else:  # daily
        start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

    return start, end
