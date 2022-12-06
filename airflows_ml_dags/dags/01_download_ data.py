import os
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
        "01_dowload_data",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=days_ago(5),
) as dag:

    start_download = DummyOperator(task_id="start-download")

    download = DockerOperator(
        image="airflow-download",
        command="--output-dir /data/raw/{{ ds }}",
        network_mode="bridge",
        task_id="docker-airflow-download",
        do_xcom_push=False,
        mount_tmp_dir=False,
        # !!! HOST folder(NOT IN CONTAINER) replace with yours !!!
        mounts=[Mount(source='/home/kate_kosareva/PycharmProjects/airflow-examples/data', target="/data", type='bind')]
        #"/Users/mikhailmar/IdeaProjects/airflow-examples/data/"

    )

    stop_download = DummyOperator(task_id="stop-download")

    start_download >> download >> stop_download
