# Backend Setup Instructions

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


    
