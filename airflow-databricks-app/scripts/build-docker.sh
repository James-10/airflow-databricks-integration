#!/bin/bash

echo "Starting ariflow-databricks Docker build"

docker build -t airflow:dev .

docker run --name airflow-databricks -d -p 8080:8080 --env-file ./.env airflow:dev bash -c "airflow db init && airflow webserver -p 8080 & airflow scheduler"

