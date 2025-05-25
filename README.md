# SaaS Log ETL Pipeline with Apache Airflow

This project demonstrates a robust ETL (Extract, Transform, Load) pipeline designed to process synthetic SaaS application logs. Leveraging **Apache Airflow** for orchestration, **PostgreSQL** for data storage, and **Docker** for containerization, the pipeline ensures modularity, scalability, and maintainability. It also integrates **Slack notifications** for real-time alerting and **GitHub Actions** for continuous integration.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [How the Pipeline Works](#how-the-pipeline-works)
- [Getting Started](#getting-started)
- [Triggering the ETL Pipeline](#triggering-the-etl-pipeline)
- [PostgreSQL Table Schema](#postgresql-table-schema)
- [Testing & CI](#testing--ci)
- [Slack Alerts](#slack-alerts)
- [Future Improvements](#future-improvements)
- [Technologies Used](#technologies-used)
- [Author](#author)
- [License](#license)

---

## Features

- **Modular ETL Components**: Separate modules for extraction, transformation, and loading.
- **Airflow Orchestration**: DAGs manage task dependencies and scheduling.
- **Slack Alerts**: Real-time notifications on task failures via Slack.
- **CI with GitHub Actions**: Automated testing pipeline for code quality assurance.
- **Dockerized Environment**: Consistent and portable development setup.

---

## Project Structure

```
saas-log-etl/
├── airflow/
│   ├── dags/
│   │   ├── log_etl_dag.py          # Airflow DAG
│   │   └── slack_alert.py          # Slack alert function
│   ├── plugins/
│   └── logs/
├── common/
│   └── file_utils.py               # Utility functions
├── config/
│   └── config.py                   
├── data/
│   ├── raw_logs/                   # Raw JSONL logs
│   └── processed_logs/             # Transformed JSONL logs
├── etl/
│   ├── extract/
│   │   └── log_generator.py        # Synthetic log generator
│   ├── transform/
│   │   └── session_transformer.py  # Log transformation logic
│   └── load/
│       └── log_loader.py           # Load logs into PostgreSQL
├── tests/
│   ├── test_log_generator.py       # Unit tests for log generation
│   ├── test_session_transformer.py # Unit tests for transformation
│   └── test_log_loader.py          # Unit tests for loading
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions workflow
├── docker-compose.yaml             # Docker Compose configuration
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## How the Pipeline Works

This ETL pipeline is orchestrated using Apache Airflow and consists of three key stages:

### 1. Extraction (`log_generator.py`)
Generates synthetic user activity logs (e.g., login, logout, purchase) and saves them in JSON Lines format to the `data/raw_logs/` directory.

Each DAG run produces a new log file using a UTC-based timestamp to ensure uniqueness and avoid overwriting:

```
data/raw_logs/log_<UTC_TIMESTAMP>.jsonl
```

### 2. Transformation (`session_transformer.py`)
Processes and enriches raw logs into a structured schema with:

- Log level (`info`, `debug`, or `critical`)
- Human-readable activity message
- Metadata: `timestamp`, `user_id`, `session_id`

Transformed logs are saved in the `data/processed_logs/` directory:

```
data/processed_logs/processed_<UTC_TIMESTAMP>.jsonl
```

Example output:

```json
{
  "timestamp": "2025-05-22T08:10:11.411599+00:00",
  "level": "info",
  "message": "User user_17 logged out",
  "user_id": "user_17",
  "session_id": "session_5361"
}
```

### 3. Loading (`log_loader.py`)
Reads the transformed log files and inserts them into a PostgreSQL database table designed for analytical querying.

The loader ensures:
- **Idempotent inserts** to prevent duplicates
- **Proper data typing and schema alignment**
- **Persistence for historical session-level activity**

This enables downstream use cases such as:
- Dashboarding via BI tools
- Ad hoc SQL analysis
- User behavior trend reporting

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/SoeRatch/saas-log-etl.git
   cd saas-log-etl
   ```

2. **Create the `.env` File**:

   Create a `.env` file in the root directory with the following environment variables:

   ```env
   # PostgreSQL
   POSTGRES_USER=airflow
   POSTGRES_PASSWORD=airflow
   POSTGRES_DB=airflow
   DB_HOST=postgres
   DB_PORT=5432
   DB_NAME=airflow
   DB_USER=airflow
   DB_PASSWORD=airflow

   # Airflow
   AIRFLOW__CORE__EXECUTOR=LocalExecutor
   AIRFLOW__CORE__FERNET_KEY=
   AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=false
   AIRFLOW__WEBSERVER__WORKERS=2
   AIRFLOW__CORE__LOAD_EXAMPLES=false
   PYTHONPATH=/opt/airflow

   ```

   > **Note**: These credentials are for local development only. Change them for production environments and avoid committing `.env` files with secrets to git.



3. **Start Docker Services**:

   On first run or after making changes to dependencies:
   ```bash
   docker compose up --build -d
   ```

   On subsequent runs, you can just start the containers:
   ```bash
   docker compose up -d
   ```

4. **Initialize Airflow (first time only):**

   ```bash
   docker compose exec airflow-webserver airflow db init
   ```

   Then create an Airflow admin user. For security and flexibility, it's recommended to use environment variables:

   ```bash
   # Set up credentials for local development (change these in production)
   export AIRFLOW_USERNAME=admin
   export AIRFLOW_PASSWORD=admin
   export AIRFLOW_EMAIL=admin@example.com

   docker compose exec airflow-webserver airflow users create \
     --username $AIRFLOW_USERNAME \
     --firstname First \
     --lastname Last \
     --role Admin \
     --email $AIRFLOW_EMAIL \
     --password $AIRFLOW_PASSWORD
   ```

   > **Note**: These credentials are for local development only. Update them accordingly for production use.

5. **Access Airflow UI**:

   Open [http://localhost:8080](http://localhost:8080) in your browser.

---

## Triggering the ETL Pipeline

1. Open the **Airflow UI**.
2. Locate the `log_etl_pipeline` DAG in the DAGs list and toggle it **"On"** to enable scheduling.
3. Click **"Trigger DAG"** to run the pipeline manually.
4. Monitor task execution in the **Graph View** or **Logs** to verify successful completion.

---

## PostgreSQL Table Schema

This project creates the following tables automatically during load:

### 1. `processed_logs`
Stores the transformed logs.

```sql
CREATE TABLE IF NOT EXISTS processed_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    level VARCHAR(20),
    message TEXT,
    user_id VARCHAR(50),
    session_id VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uniq_log_event UNIQUE (timestamp, user_id, session_id)
);
```

### 2. `etl_runs`
Tracks metadata for each ETL run including execution timestamp, load status, and row count.

```sql
CREATE TABLE IF NOT EXISTS etl_runs (
    id SERIAL PRIMARY KEY,
    execution_date TIMESTAMPTZ,
    records_loaded INTEGER,
    status VARCHAR(20),
    message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

> No manual table setup is required. Both tables are created automatically if they do not exist.

---

## Testing & CI

- **Unit Tests**: Implemented using `pytest` for each ETL component. Tests are located in the `tests/` directory.
- **Continuous Integration**: GitHub Actions workflow (`.github/workflows/ci.yml`) triggers on push and pull requests to run tests automatically.

---

## Slack Alerts

Set up Slack notifications for task failures:

1. **Create a Slack Incoming Webhook**:
   - Navigate to [Slack API: Incoming Webhooks](https://api.slack.com/messaging/webhooks).
   - Create a new app and enable incoming webhooks.
   - Add a new webhook to your desired channel and copy the webhook URL.

2. **Configure Airflow**:
   - In the Airflow UI, go to `Admin > Variables`.
   - Add a new variable:
     - **Key**: `SLACK_WEBHOOK_URL`
     - **Value**: *Your Slack webhook URL*

3. **Alert Function**:
   - Implement a function in `airflow/dags/slack_alert.py` to send messages to Slack using the webhook URL.
   - Use this function as the `on_failure_callback` in your DAGs or tasks.

---

## Future Improvements

- **Data Validation**: Implement data quality checks using tools like Great Expectations.
- **Monitoring**: Integrate with tools such as Prometheus and Grafana for enhanced observability.
- **Cloud Deployment**: Deploy the pipeline to cloud platforms like AWS or GCP for scalability.
- **Real-time Processing**: Incorporate streaming data processing using Apache Kafka or similar.

---

## Technologies Used

- **Apache Airflow** — Workflow orchestration
- **PostgreSQL** — Data storage
- **Docker** — Containerization
- **Python** — Scripting and ETL logic
- **Slack API** — Notifications
- **GitHub Actions** — Continuous integration

---

## Author

[SoeRatch](https://github.com/SoeRatch)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
