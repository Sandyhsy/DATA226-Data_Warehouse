from airflow import DAG
from airflow.models import Variable
from airflow.decorators import task

from datetime import timedelta
from datetime import datetime
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
import requests


def return_snowflake_conn():

    # Initialize the SnowflakeHook
    hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')

    # Execute the query and fetch results
    conn = hook.get_conn()
    return conn.cursor()


@task
def train(cur, train_input_table, train_view, forecast_function_name):
    """
     - Create a view with training related columns
     - Create a model with the view above
    """

    create_view_sql = f"""
    CREATE OR REPLACE VIEW {train_view} AS 
    SELECT
        DATE, CLOSE
    FROM {train_input_table};"""

    create_model_sql = f"""
    CREATE OR REPLACE SNOWFLAKE.ML.FORECAST {forecast_function_name} (
        INPUT_DATA => SYSTEM$REFERENCE('VIEW', '{train_view}'),
        TIMESTAMP_COLNAME => 'DATE',
        TARGET_COLNAME => 'CLOSE',
        CONFIG_OBJECT => {{'ON_ERROR': 'SKIP'}}
    );
    """
    try:
        cur.execute(create_view_sql)
        cur.execute(create_model_sql)
        # Inspect the accuracy metrics of your model. 
        cur.execute(f"CALL {forecast_function_name}!SHOW_EVALUATION_METRICS();")

    except Exception as e:
        print(e)
        raise


@task
def predict(cur, forecast_function_name, train_input_table, forecast_table, final_table):
    """
    Generate predictions for the next 7 weeks and store the results to a table named forecast_table.
    The final table combines historical stock data with predictions and includes lower and upper bounds.
    EMA is included as a feature in the model for forecasting.
    """

    # Step 1: Create the forecast using Snowflake ML Function (for weekly data, using EMA as a feature)
    make_prediction_sql = f"""
    BEGIN
        -- This is the step that creates your predictions using the forecasting model, including EMA as a feature.
        CALL {forecast_function_name}!FORECAST(
            FORECASTING_PERIODS => 7,  -- Forecast for the next 7 weeks
            CONFIG_OBJECT => {{'prediction_interval': 0.95}}  -- Set prediction interval to 95%
        );
        
        -- Store the generated predictions into a table
        LET x := SQLID;  -- Get the result set's SQLID
        CREATE TABLE IF NOT EXISTS {forecast_table} AS 
        SELECT * FROM TABLE(RESULT_SCAN(:x));  -- Extract the forecast data
    
    END;
    """

    # Step 2: Create the final table combining actual weekly data and forecasted values
    create_final_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {final_table} AS
    SELECT 
        SYMBOL, 
        DATE, 
        CLOSE AS actual, 
        NULL AS forecast, 
        NULL AS lower_bound, 
        NULL AS upper_bound
    FROM {train_input_table}  -- Historical data (weekly data with EMA as a feature)
    
    UNION ALL
    
    SELECT 
        REPLACE(series, '"', '') AS SYMBOL,  -- Remove quotes from symbol
        ts AS DATE,  -- Weekly forecast dates
        NULL AS actual,  -- No actual value for predictions
        forecast, 
        lower_bound, 
        upper_bound
    FROM {forecast_table};  -- Predicted weekly data
    """

    try:
        # Step 3: Execute the SQL to generate predictions and store them
        cur.execute(make_prediction_sql)
        print("Prediction process completed successfully.")
        
        # Step 4: Create the final table combining actual and forecasted data
        cur.execute(create_final_table_sql)
        print(f"Final table '{final_table}' created successfully.")
    
    except Exception as e:
        # Handle any errors during execution
        print(f"Error occurred: {e}")
        raise


with DAG(
    dag_id = 'TrainPredict',
    start_date = datetime(2025,2,21),
    catchup=False,
    tags=["Lab1_forecast"],
    schedule = '30 2 * * *'
) as dag:
    train_input_table = "dev.raw.stock_price_lab"
    train_view = "dev.raw.stock_price_lab_view"
    forecast_table = "dev.raw.stock_price_lab_forecast"
    forecast_function_name = "dev.analytics.amazon_stock_prediction"
    final_table = "dev.analytics.amazon_stock"
    
    cur = return_snowflake_conn()

    train(cur, train_input_table, train_view, forecast_function_name)
    predict(cur, forecast_function_name, train_input_table, forecast_table, final_table)
