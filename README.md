# SaaS Log ETL Pipeline with Apache Airflow

This project simulates an ETL (Extract, Transform, Load) pipeline for SaaS application logs using Apache Airflow, PostgreSQL, and Docker. The pipeline:

1. **Extracts** synthetic user log events (e.g., login, logout, purchase)
2. **Transforms** them into enriched, readable log entries
3. **Loads** them into a PostgreSQL database

---

## 🛠️ Project Structure

```
project-root/
├── airflow/
│   ├── dags/
│   │   └── log_etl_dag.py           # Main Airflow DAG
│   ├── plugins/
│   └── logs/
├── data/
│   ├── raw_logs/                    # Raw JSONL logs
│   └── processed_logs/             # Transformed JSONL logs
├── etl/
│   ├── extract/
│   │   └── log_generator.py         # Synthetic log generator
│   ├── transform/
│   │   └── session_transformer.py   # Log enricher
│   └── load/
│       └── loader.py                # PostgreSQL loader
├── docker-compose.yaml
└── README.md
```

---

## ⚙️ Technologies Used

- 🌀 **Apache Airflow** — DAG scheduling and orchestration
- 🐳 **Docker Compose** — Local development and service containerization
- 🐘 **PostgreSQL** — Structured data storage
- 🐍 **Python** — Custom ETL logic
- 📁 **JSON Lines (JSONL)** — Log file format

---

## 🧪 How the Pipeline Works

### ▶️ 1. Extraction (`log_generator.py`)

Generates synthetic SaaS log events (login/logout/purchase) in JSONL format. Logs are timestamped and saved like:

```
/opt/airflow/data/raw_logs/log_20250522_081657.jsonl
```

Each DAG run creates a new log file using UTC time to avoid overwriting.

---

### 🔄 2. Transformation (`session_transformer.py`)

Parses and enriches raw log events into a structured format:

- Assigns a log level (`info`, `debug`, `critical`)
- Adds human-readable messages
- Preserves metadata: `timestamp`, `user_id`, `session_id`

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

---

### 🧩 3. Load (`loader.py`)

- Reads the transformed logs
- Ensures the PostgreSQL table `processed_logs` exists
- Inserts all entries into the database

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/SoeRatch/saas-log-etl.git
cd saas-log-etl
```

### 2. Start Docker Services

```bash
docker-compose up --build
```

### 3. Initialize Airflow (first time only)

```bash
docker compose exec airflow-webserver airflow db init

docker compose exec airflow-webserver airflow users create \
  --username admin \
  --firstname First \
  --lastname Last \
  --role Admin \
  --email admin@example.com \
  --password admin
```

Access Airflow at: [http://localhost:8080](http://localhost:8080)

---

## 🧪 Triggering the ETL Pipeline

1. Navigate to the Airflow UI
2. Enable the `log_etl_pipeline` DAG
3. Trigger it manually (calendar icon)
4. Watch task logs and validate success

---

## 🗄️ Verifying the Loaded Data

Connect to the PostgreSQL DB using a tool like **DBeaver**:

- Host: `localhost`
- Port: `5432`
- Database: `airflow`
- User: `airflow`
- Password: `airflow`

Check the `public.processed_logs` table under the `airflow` schema.

---

## ✅ PostgreSQL Table Schema

```sql
CREATE TABLE IF NOT EXISTS processed_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    level VARCHAR(20),
    message TEXT,
    user_id VARCHAR(50),
    session_id VARCHAR(50)
);
```

---

## ✅ Status

- ✅ Extract step complete (fake SaaS logs written daily)
- ✅ Transform step complete (log level + message enrichment)
- ✅ Load step complete (PostgreSQL insert + schema creation)

---

## 📦 Future Improvements

- Add data validation & schema enforcement
- Add automated tests for each ETL step
- Introduce partitioning/indexing for faster queries
- Parameterize configs using `.env` or Airflow Variables
- Integrate with cloud data warehouse (e.g., BigQuery, Redshift)

---

## 👨‍💻 Author

[SoeRatch](https://github.com/SoeRatch)

---

## 📜 License

MIT License
