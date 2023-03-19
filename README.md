# Airflow-Databricks-Integration
Integrate Databricks and airflow by executing code directly on Databricks using an Airflow DAG

## About
This project uses the airflow community [docker-compose](https://airflow.apache.org/docs/apache-airflow/2.5.2/docker-compose.yaml) configuration. This is a basic POC for Airflow DAGs' integration with Databricks using the `databricks-cli` trigger the databricks api endpoints.

The `notebooks/` folder holds some sample python modules to execute in Databricks and the `dags/` folder has sample DAGS to create/execute the notebooks in Databricks

## Dependencies
- `Docker`
- a Databricks account
- `pipenv` for python dependencies

This project assumes you have working knowledge of these technogogies.

## Run
Open a terminal in the project root directory: `airflow-databricks-app`. 

To start the application locally:
1. Shell into the pipenv virtual environment and install dependencies: `pipenv shell && pipenv install`
2. Create a `.env` file: `pipenv run env` or `cp .env.example .env`
3. Add your Databricks and Airflow configs to the `env` file
4. Execute: `pipenv run up`
5. Open the Airflow webserver at: http://localhost:8080 to see the dags created

To stop the docker deployment, execute: `pipenv run down`


### Author
James Ockhuis (ockhuisjames@gmail.com)
