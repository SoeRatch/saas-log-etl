import json
import requests
from airflow.models import Variable

def slack_alert_fn(context):
    # Store SLACK_WEBHOOK_URL in Airflow UI → Admin → Variables
    slack_webhook = Variable.get("SLACK_WEBHOOK_URL")
    task_instance = context.get('task_instance')
    dag_id = context.get('dag').dag_id
    task_id = context.get('task_instance').task_id
    execution_date = context.get('execution_date')
    try_number = context.get('task_instance').try_number

    message = {
        "text": (
            f":x: *Task Failed!* \n"
            f"> *DAG*: `{dag_id}`\n"
            f"> *Task*: `{task_id}`\n"
            f"> *Execution Date*: `{execution_date}`\n"
            f"> *Try Number*: `{try_number}`"
        )
    }

    requests.post(slack_webhook, data=json.dumps(message))
