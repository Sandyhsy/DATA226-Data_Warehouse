from airflow import DAG
from airflow.models import Variable
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime
import snowflake.connector
import requests
import pandas as pd
import io

# Function to return Snowflake connection
def return_snowflake_conn():

    # Initialize the SnowflakeHook
    hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')

    # Execute the query and fetch results
    conn = hook.get_conn()
    return conn.cursor()


@task
def extract_data(url):
    response = requests.get(url)
    response.raise_for_status()
    
    df = pd.read_csv(io.StringIO(response.text))
    print(f"Extracted {len(df)} rows from CSV.")
    return df.to_dict(orient='records')


@task
def transform_data(raw_data):
    df = pd.DataFrame(raw_data)

    # Convert datetime fields
    for col in ['received_datetime', 'enroute_datetime', 'dispatch_datetime', 'onscene_datetime']:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # The columns to keep    
    df = df[['id', 'cad_number', 'received_datetime', 'enroute_datetime',
            'dispatch_datetime', 'onscene_datetime', 'agency', 'police_district']]

    # Drop rows with missing critical values
    df = df.dropna(subset=['received_datetime', 'enroute_datetime','dispatch_datetime', 'onscene_datetime', 'agency', 'police_district'])

    # Calculate response time in minutes
    df['dispatch_to_received_min'] = (df['dispatch_datetime'] - df['received_datetime']).dt.total_seconds() / 60.0
    df['enroute_to_dispatch_min'] = (df['enroute_datetime'] - df['dispatch_datetime']).dt.total_seconds() / 60.0
    df['onscene_to_enroute_min'] = (df['onscene_datetime'] - df['enroute_datetime']).dt.total_seconds() / 60.0


    for col in ['received_datetime', 'enroute_datetime', 'dispatch_datetime', 'onscene_datetime']:
        df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
        
    return df.to_dict(orient='records')


@task
def load_data(cur, records, database, schema, table):
    try:
        cur.execute("BEGIN;")
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {database}.{schema}.{table} (
                id STRING,
                cad_number STRING,
                received_datetime TIMESTAMP,
                dispatch_datetime TIMESTAMP,
                onscene_datetime TIMESTAMP,
                police_district STRING,
                dispatch_to_received_min FLOAT, 
                enroute_to_dispatch_min FLOAT, 
                onscene_to_enroute_min FLOAT
            );
        """)
        cur.execute(f"DELETE FROM {database}.{schema}.{table}")

        insert_stmt = f"""
            INSERT INTO {database}.{schema}.{table} VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        for row in records:
            cur.execute(insert_stmt, tuple(row.get(col) for col in [
                "id", "cad_number", "received_datetime", "dispatch_datetime",
                "onscene_datetime", "police_district", "dispatch_to_received_min",
                "enroute_to_dispatch_min", "onscene_to_enroute_min"
            ]))
        cur.execute("COMMIT;")
    except Exception as e:
        cur.execute("ROLLBACK;")
        raise e


# Define DAG
with DAG(
    dag_id='law_enforcement_ETL',
    start_date=datetime(2025,4,20),
    catchup=False,
    tags=['ETL', 'law_enforcement'],
    schedule='30 2 * * *'
) as dag:
    cur = return_snowflake_conn()
    
    url = Variable.get("lab2_LawInforcement_url")
    database = Variable.get("database")
    schema = Variable.get("schema_name")
    table = "law_enforcement_calls"

    extract = extract_data(url)
    transform = transform_data(extract)
    load = load_data(cur, transform, database, schema, table)
    
    extract >> transform >> load