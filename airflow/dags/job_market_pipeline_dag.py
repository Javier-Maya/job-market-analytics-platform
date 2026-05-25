import os
from datetime import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator


with DAG(
    dag_id="job_market_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["job-market"],
) as dag:

    run_pipeline = DockerOperator(
        task_id="run_pipeline",
        image="job-market-worker:latest",
        command="python -m app.pipeline.run_pipeline",
        docker_url="unix://var/run/docker.sock",
        network_mode="job-analytics-platform_job_market_network",
        auto_remove=True,
        mount_tmp_dir=False,
        environment={
            "DB_HOST": os.getenv("DB_HOST", "postgres"),
            "DB_NAME": os.getenv("DB_NAME", "job_analytics"),
            "DB_USER": os.getenv("DB_USER", "job_user"),
            "DB_PASSWORD": os.getenv("DB_PASSWORD", "job_password"),
            "DB_PORT": os.getenv("DB_PORT", "5432"),
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "AWS_DEFAULT_REGION": os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            "S3_BUCKET_NAME": os.getenv("S3_BUCKET_NAME"),
        },
    )