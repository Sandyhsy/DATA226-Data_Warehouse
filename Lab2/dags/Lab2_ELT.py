from pendulum import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator



with DAG(
    dag_id="law_enforcement_ELT_dbtcloud",
    start_date=datetime(2025, 4, 20),
    description="A DAG to run dbt Cloud job via Airflow",
    schedule='30 2 * * *',
    catchup=False,
) as dag:

    trigger_dbt_cloud_job = DbtCloudRunJobOperator(
        task_id = "trigger_dbt_job",
        job_id = Variable.get("dbt_cloud_job_id"),  # Set this in Airflow Variables
        check_interval = 30,  # polling interval (in seconds)
        timeout = 300,        # total timeout in seconds
        dbt_cloud_conn_id = "dbt_cloud"  # Set this in Airflow Connections
    )