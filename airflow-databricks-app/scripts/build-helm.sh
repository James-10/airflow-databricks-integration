## set the release-name & namespace
helm repo add airflow-stable https://airflow-helm.github.io/charts
helm repo update

export AIRFLOW_NAME="airflow-cluster"

if ! minikube status 
then
    minikube delete
    minikube start
fi

## install using helm 3
helm install "$AIRFLOW_NAME" airflow-stable/airflow --version "8.6.1" -f airflow-helm/values.yaml
