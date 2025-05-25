import os

def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Required environment variable '{var_name}' not set.")
    return value

def get_db_config():
    return {
        "dbname": get_env_variable("DB_NAME"),
        "user": get_env_variable("DB_USER"),
        "password": get_env_variable("DB_PASSWORD"),
        "host": get_env_variable("DB_HOST"),
        "port": get_env_variable("DB_PORT"),
    }
