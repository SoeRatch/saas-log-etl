# SaaS Log ETL Pipeline with Apache Airflow

This project simulates an ETL (Extract, Transform, Load) pipeline for SaaS application logs using Apache Airflow and Docker. The pipeline:

1. **Extracts** synthetic user log events (e.g., login, logout, purchase)
2. **Transforms** them into enriched, readable log entries
3. **Load** them into a structured storage system (e.g., PostgreSQL)


## 🛠️ Project Structure



## Backend Setup Instructions

Before starting the backend development, follow these steps to set up and activate a virtual environment:

## 🔧 Setting up the Virtual Environment

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**

   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. Make sure to add the `venv` directory to your `.gitignore` file to avoid committing environment-specific files to version control.

    - 📄 Example `.gitignore` entry:
    ```
    venv/
    ```


## 🛠️ Log File Generation with Faker

To simulate log data for backend development, follow these steps:

1. **Install Faker**

    - Make sure your virtual environment is activated, then run:
      ```bash
      pip install faker
      ```

2. **Generate Log Files**

    - Run the following script to extract/generate log files:
    ```bash
    python etl/extract/log_generator.py
    ```

    This will create log files in the `data/raw_logs/` directory.

3. **Update `.gitignore`**

    - To avoid committing generated log files, add the following entry to your `.gitignore`:
    ```
    data/raw_logs/
    ```



## 🛠️ Setup Airflow with docker

To simulate log data for backend development, follow these steps:

1. **Create required files and folders**
    ```bash
    touch docker-compose.yaml
    mkdir -p airflow/dags airflow/logs airflow/plugins
    ```

2. **Initialize Airflow**

    - Start Airflow Services (Webserver & Scheduler):
    The Airflow scheduler executes your tasks on an array of workers
    ```bash
    docker compose up airflow-webserver airflow-scheduler --build --detach
    ```
    This will spin up the webserver and scheduler containers in detached mode.
    It also builds the images
    It will use your docker-compose.yaml at the root

    -  Initialize Airflow metadata DB:
    ```bash
    docker compose exec airflow-webserver airflow db init
    ```
    This creates the metadata database (e.g., task instances, DAG run history, etc.).
    You only need to run this once on first setup (unless you wipe the database).

    -  Create admin user:
    ```
    docker compose exec airflow-webserver airflow users create \
    --username admin \
    --firstname First \
    --lastname Last \
    --role Admin \
    --email admin@example.com \
    --password admin

    ```

3. **Run Airflow**
    - Run airflow
    ```
    docker compose up
    ```

    - Then open your browser and go to:
    ```
    http://localhost:8080
    ```

    - Login with the username and password created.

    - Restart airflow
    ```
    docker compose down
    docker compose up -d
    ```

4. **Database setup**
    Create table inside the PostgreSQL container that's already running via Docker Compose.

    - Run this from your terminal:
    ```
    docker compose exec postgres psql -U airflow -d airflow
    ```

    - Then manually run SQL like:
    ```
    CREATE TABLE IF NOT EXISTS processed_logs (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMPTZ,
        level VARCHAR(20),
        message TEXT,
        user_id VARCHAR(50),
        session_id VARCHAR(50)
    );

    ```


    
