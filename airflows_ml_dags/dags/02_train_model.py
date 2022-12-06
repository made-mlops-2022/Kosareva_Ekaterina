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
        "02_train_model",
        default_args=default_args,
        schedule_interval="@weekly",
        start_date=days_ago(10),
) as dag:

    start_train = DummyOperator(task_id="start-train")

    preprocess = DockerOperator(
        image="airflow-preprocess",
        command="--input-dir /data/raw/{{ ds }} --output-dir /data/processed/{{ ds }}",
        task_id="docker-airflow-preprocess",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source='/home/kate_kosareva/PycharmProjects/airflow-examples/data', target="/data", type='bind')]
    )

    train = DockerOperator(
        image="airflow-train",
        command="--input-dir /data/processed/{{ ds }} --model-dir /data/models/{{ ds }}",
        task_id="docker-airflow-train",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source='/home/kate_kosareva/PycharmProjects/airflow-examples/data', target="/data", type='bind')]
    )

    validate = DockerOperator(
        image="airflow-validate",
        command="--input-dir /data/processed/{{ ds }} --model-dir /data/models/{{ ds }}",
        task_id="docker-airflow-validate",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source='/home/kate_kosareva/PycharmProjects/airflow-examples/data', target="/data", type='bind')]
    )

    stop_train = DummyOperator(task_id="stop-train")

    start_train >> preprocess >> train >> validate >> stop_train
