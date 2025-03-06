# In Cloud Composer, add apache-airflow-providers-snowflake to PYPI Packages
from airflow import DAG
from airflow.models import Variable
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

from datetime import timedelta
from datetime import datetime
import snowflake.connector
import requests

import json

def return_snowflake_conn():

    # Initialize the SnowflakeHook
    hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')

    # Execute the query and fetch results
    conn = hook.get_conn()
    return conn.cursor()

@task
def extract(url):
    # f = requests.get(url)
    # return (f.text)

    f = requests.get(url)
    data = f.json()
    return data


@task
def transform(text):
    # data = json.loads(text)
    records = []
    for d in text["Time Series (Daily)"]:
        stock_info = text["Time Series (Daily)"][d]
    #   stock_info["date"] = d
    #   stock_info["lab_symbol"] = Variable.get("lab_symbol")
        record = {
            "symbol": Variable.get("lab_symbol"),
            "date": d,
            "open": stock_info["1. open"],
            "close": stock_info["4. close"],
            "high": stock_info["2. high"],
            "low": stock_info["3. low"],
            "volume": stock_info["5. volume"]
        }
        records.append(record)
        if len(records) >= 90:
            break

    return records



@task
def load(cur, records, target_table):
    try:
        cur.execute("BEGIN;")
        cur.execute(f"CREATE TABLE IF NOT EXISTS {target_table} (symbol VARCHAR(10), date DATE, open FLOAT, close FLOAT, high FLOAT, low FLOAT, volume BIGINT, PRIMARY KEY (symbol, date));")
        cur.execute(f"DELETE FROM {target_table}")
        for r in records:
          symbol = r["symbol"]
          date = r["date"]
          open = r["open"]
          close = r["close"]
          high = r["high"]
          low = r["low"]
          volume = r["volume"]

          insert_sql = f"INSERT INTO {target_table} (symbol, date, open, close, high, low, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
          cur.execute(insert_sql, (symbol, date, open, close, high, low, volume))
        cur.execute("COMMIT;")
    except Exception as e:
        cur.execute("ROLLBACK;")
        print(e)
        raise e


with DAG(
    dag_id = 'Lab1_ETL_StockPrice',
    start_date = datetime(2024,9,21),
    catchup=False,
    tags=['ETL'],
    schedule = '30 2 * * *'
) as dag:
    target_table = "dev.raw.stock_price_lab"
    url = Variable.get("lab_stock_price_url")
    cur = return_snowflake_conn()

    data = extract(url)
    lines = transform(data)
    load(cur, lines, target_table)
