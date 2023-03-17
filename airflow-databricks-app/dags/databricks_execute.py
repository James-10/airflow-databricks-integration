import os
import json
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from databricks_cli.jobs.api import JobsApi
from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.workspace.api import WorkspaceApi


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
}

dag = DAG(
    'databricks_notebook_example',
    default_args=default_args,
    description='DAG to run a Databricks notebook',
    schedule_interval=None,
)

username = os.environ.get("user")
notebook_name = 'airflow_notebook'
notebook_module = "airflow_notebook.py"
notebooks_folder = f"{os.path.dirname(os.path.dirname(__file__))}/notebooks/"
module_path = f"{notebooks_folder}{notebook_module}"
databricks_notebook_path = f"/Users/{username}/{notebook_name}"


api_client = ApiClient(
  host  = os.environ.get("databricks_host"),
  token = os.environ.get("databricks_token")
 )
ws = WorkspaceApi(api_client)
job = JobsApi(api_client)


def create_notebook_from_module():
    """Create a databricks notebook from a python module"""

    try:
        ws.import_workspace(
            source_path=module_path,
            target_path=databricks_notebook_path,
            is_overwrite=False,
            language="PYTHON",
            fmt="SOURCE",
        )
        print(f"successfully created notebook: {notebook_name}")
    except Exception as err:
        print(err)
        raise

def create_notebook_job(**context):
    """Create a databricks job for a notebook"""

    task_instance = context['ti']
    job_config = json.dumps(
        {'name': 'airflow_job',
        'new_cluster': {
            'spark_version': "11.0.x-scala2.12",
            'node_type_id': 'Standard_DS3_v2',
            'num_workers': 2,
            'spark_conf': {
                "spark.master": "local[*]"
            }
        },
        'notebook_task': {
            'notebook_path': databricks_notebook_path,
            "source": "WORKSPACE"
        }
    })

    job_id = job.create_job(json=job_config)
    task_instance.xcom_push(key='notebook_job_id', value=job_id)

def run_notebook(**context):
    """Run a databricks notebook as a job"""

    task_instance = context['ti']
    job_id = task_instance.xcom_pull(key="notebook_job_id")
    job.run_now(job_id=job_id)


def delete_notebook():
    """Delete a databricks notebook"""
    try:
        response = ws.delete(
            workspace_path=databricks_notebook_path,
        )
        print(response)
    except Exception as err:
        print(err)
        raise


create_notebook_task = PythonOperator(
    task_id='create_notebook_task',
    dag=dag,
    python_callable=create_notebook_from_module,
)


create_dbricks_job_task = PythonOperator(
    task_id='create_databricks_job_task',
    dag=dag,
    python_callable=create_notebook_job,
)


run_notebook_task = PythonOperator(
    task_id='run_notebook_task',
    dag=dag,
    python_callable=run_notebook
)


delete_notebook_task = PythonOperator(
    task_id='delete_notebook_task',
    dag=dag,
    python_callable=delete_notebook
)


create_notebook_task >> create_dbricks_job_task  >> run_notebook_task >> delete_notebook_task