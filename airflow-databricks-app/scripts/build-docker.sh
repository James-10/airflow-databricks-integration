#!/bin/bash

echo "Starting ariflow-databricks Docker build"

docker build -t airflow-databricks:dev .

docker compose -f ../deployment/docker-compose.yaml up airflow-init
docker compose -f ../deployment/docker-compose.yaml up -d
