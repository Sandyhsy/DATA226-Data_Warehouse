from airflow import DAG
from airflow.models import Variable
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime
import snowflake.connector

# Function to return Snowflake connection
def return_snowflake_conn():

    # Initialize the SnowflakeHook
    hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')

    # Execute the query and fetch results
    conn = hook.get_conn()
    return conn.cursor()

@task
def create_tables(database, schema, table_channel, table_timestamp):
    """Creates the required tables in Snowflake."""
    cur = return_snowflake_conn()
    try:
        cur.execute("BEGIN;")
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {database}.{schema}.{table_channel} (
            userId INT NOT NULL,
            sessionId VARCHAR(32) PRIMARY KEY,
            channel VARCHAR(32) DEFAULT 'direct'
        );
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {database}.{schema}.{table_timestamp} (
            sessionId VARCHAR(32) PRIMARY KEY,
            ts TIMESTAMP
        );
        """)
        cur.execute("COMMIT;")
    except Exception as e:
        cur.execute("ROLLBACK;")
        print("Error creating tables:", e)
        raise e

@task
def load_data(database, schema, table_channel, table_timestamp):
    """Loads data from S3 into Snowflake tables."""
    cur = return_snowflake_conn()
    try:
        cur.execute("BEGIN;")
        cur.execute(f"""
            COPY INTO {database}.{schema}.{table_channel}
            FROM @dev.raw.blob_stage/{table_channel}.csv
            FILE_FORMAT = (TYPE = CSV, SKIP_HEADER = 1, FIELD_OPTIONALLY_ENCLOSED_BY = '"');    
        """)
        cur.execute(f"""
            COPY INTO {database}.{schema}.{table_timestamp}
            FROM @dev.raw.blob_stage/{table_timestamp}.csv
            FILE_FORMAT = (TYPE = CSV, SKIP_HEADER = 1, FIELD_OPTIONALLY_ENCLOSED_BY = '"');
        """)
        cur.execute("COMMIT;")
    except Exception as e:
        cur.execute("ROLLBACK;")
        print("Error loading data:", e)
        raise e

# Define DAG
with DAG(
    dag_id='ETL',
    start_date=datetime(2025,3,10),
    catchup=False,
    tags=['ETL'],
    schedule='30 2 * * *'
) as dag:

    database = "USER_DB_LION"
    schema = "raw"
    table_channel = "user_session_channel"
    table_timestamp = "session_timestamp"
    
    create_snowflake_tables = create_tables(database, schema, table_channel, table_timestamp)
    load_snowflake_data = load_data(database, schema, table_channel, table_timestamp)
