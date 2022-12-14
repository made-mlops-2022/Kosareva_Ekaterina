import os
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.dummy import DummyOperator
from airflow.sensors.python import PythonSensor
from airflow.utils.dates import days_ago
from docker.types import Mount

def wait_for_file(file_name):
    return os.path.exists(file_name)


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
    
    waiting_data = PythonSensor(
        task_id="waiting_data",
        python_callable=wait_for_file,
        op_args=["/opt/airflow/data/raw/{{ ds }}/data.csv"],
        timeout=6000,
        poke_interval=10,
        retries=100,
        mode="poke"
    )

    preprocess = DockerOperator(
        image="airflow-preprocess",
        command="--input-dir /data/raw/{{ ds }} --output-dir /data/processed/{{ ds }}",
        task_id="docker-airflow-preprocess",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source='/home/kate_kosareva/PycharmProjects/airflows_ml_dags/data', target="/data", type='bind')]
    )

    train = DockerOperator(
        image="airflow-train",
        command="--input-dir /data/processed/{{ ds }} --model-dir /data/models/{{ ds }}",
        task_id="docker-airflow-train",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source='/home/kate_kosareva/PycharmProjects/airflows_ml_dags/data', target="/data", type='bind')]
    )

    validate = DockerOperator(
        image="airflow-validate",
        command="--input-dir /data/processed/{{ ds }} --model-dir /data/models/{{ ds }}",
        task_id="docker-airflow-validate",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source='/home/kate_kosareva/PycharmProjects/airflows_ml_dags/data', target="/data", type='bind')]
    )

    stop_train = DummyOperator(task_id="stop-train")

    start_train >> waiting_data>> preprocess >> train >> validate >> stop_train
