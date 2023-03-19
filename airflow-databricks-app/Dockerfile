FROM apache/airflow:2.5.2-python3.10

WORKDIR /airflow-databricks

COPY Pipfile Pipfile.lock /airflow-databricks/

RUN pip install pipenv

RUN pipenv install --system --deploy

COPY . /airflow-databricks/

COPY ./dags/ /opt/airflow/dags

CMD []