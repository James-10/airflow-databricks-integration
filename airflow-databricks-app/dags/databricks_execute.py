import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.providers.databricks.hooks.databricks import DatabricksHook

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

notebook_name = 'notebook_test'
module_path = os.path.dirname(os.path.dirname(__file__)).join('notebook_test.py')
hook = DatabricksHook()


def create_empty_notebook():
    notebook_content = {
        "content": "",
        "path": notebook_name
    }

    hook.run_now(endpoint='notebooks/create', json=notebook_content)

def update_notebook():

    with open(module_path, 'r') as f:
        module_contents = f.read()

    notebook_update_content = {
        "content": module_contents,
        "path": notebook_name,
        "language": "PYTHON"
    }

    hook.run_now(endpoint='notebooks/import', json=notebook_update_content)

def delete_notebook():

    delete_notebook_content = {
        "path": notebook_name
    }

    hook.run(endpoint='notebooks/delete', json=delete_notebook_content)

create_notebook_task = PythonOperator(
    task_id='create_notebook_task',
    dag=dag,
    python_callable=create_empty_notebook,
)

update_notebook_task = PythonOperator(
    task_id='update_notebook_task',
    dag=dag,
    python_callable=update_notebook,
)

run_notebook_task = DatabricksRunNowOperator(
    task_id='run_notebook_task',
    dag=dag,
    notebook_task={'notebook_path': notebook_name},
)

delete_notebook_task = PythonOperator(
    task_id='delete_notebook_task',
    dag=dag,
    python_callable=delete_notebook
)

create_notebook_task >> update_notebook_task >> run_notebook_task >> delete_notebook_task
