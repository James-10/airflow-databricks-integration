import os
from datetime import datetime

from airflow import DAG
from airflow import settings
from airflow.models.connection import Connection
from airflow.providers.databricks.operators.databricks import DatabricksHook
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator, DatabricksSubmitRunOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
}

dag = DAG(
    dag_id="postgres_data_loader",
    default_args=default_args,
    description="Import data from AWS postgres into Databricks",
    schedule_interval=None,
)

connection_id = "elevate_airflow_dbricks"
databircks_host  = os.environ.get("databricks_host"),
databricks_token = os.environ.get("databricks_token")
username = os.environ.get("user")


def cache_databricks_connection(connection_id: str):
    """ Cache databricks connection to airflow session"""
    conn = Connection(
    conn_id=connection_id,
    conn_type="databricks",
    login=username,
    password=databricks_token
    )

    session = settings.Session()
    session.add(conn)
    session.commit()


def create_notebook(notebook_name: str, source_path: str, destination_path, connection_id: str):
    hook = DatabricksHook(databricks_conn_id=connection_id)
