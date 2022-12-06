import os
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.dummy import DummyOperator
from airflow.sensors.python import PythonSensor
from airflow.utils.dates import days_ago
from docker.types import Mount


default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
        "03_predict_class",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=days_ago(5),
) as dag:

    start_predict = DummyOperator(task_id="start-prediction")

    predict = DockerOperator(
        image="airflow-predict",
        command="--input-dir /data/raw/{{ ds }} --output-dir /data/predicted/{{ ds }} --model-dir /data/models/{{ ds }}",
        task_id="docker-airflow-predict",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source='/home/kate_kosareva/PycharmProjects/airflow-examples/data', target="/data", type='bind')]
    )

    stop_predict = DummyOperator(task_id="stop-prediction")

    start_predict >> predict >> stop_predict
