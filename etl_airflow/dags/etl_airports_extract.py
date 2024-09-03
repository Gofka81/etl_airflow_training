import os

from airflow import DAG
from datetime import datetime
from custom_operators.flight_radar_operator import FlightRadarOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from utils.s3_utils import load_parquet_to_postgres


TEMP_MINIO_BUCKET = os.getenv("TEMP_MINIO_BUCKET")
TRANSFORM_MINIO_BUCKET = os.getenv("TRANSFORM_MINIO_BUCKET")
MINIO_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL")
MINIO_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY_ID")
MINIO_SECRET_ACCESS_KEY = os.getenv("MINIO_SECRET_ACCESS_KEY")
TEMP_BUCKET_KEY = '{{dag.dag_id}}/timestamp={{ execution_date.strftime("%m-%d-%Y_%H:%M:%S") }}/{{dag.params.name}}.json'
TRANSFORM_BUCKET_KEY = '{{dag.dag_id}}/timestamp={{ execution_date.strftime("%m-%d-%Y_%H:%M:%S") }}'

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

extract_route = {
    "name": "airports",
    "route": "airports"
}


# Define the DAG
with DAG(
        dag_id='pipeline_airports_extract',
        default_args=default_args,
        description='Extract airports data',
        schedule_interval='@monthly',
        start_date=datetime(2023, 8, 30),
        catchup=False,
        tags=['etl', 'airports'],
        params=extract_route
) as dag:

    extract_task = FlightRadarOperator(
        task_id='extract_airports',
        route=extract_route["route"],
        src_bucket=TEMP_MINIO_BUCKET,
        dag=dag
    )

    sensor_extract = S3KeySensor(
        task_id=f'sensor_{extract_route["name"]}',
        bucket_name=TEMP_MINIO_BUCKET,
        bucket_key=TEMP_BUCKET_KEY,
        aws_conn_id="minio_s3"
    )

    etl_transform = SparkSubmitOperator(
        task_id=f'etl_{extract_route["name"]}_transform',
        application='/opt/bitnami/spark/jobs/src/transform/etl_airports_transform.py',
        name='pyspark_job_name',
        conn_id='spark_default',
        jars='/opt/bitnami/spark/jars/hadoop-aws-3.3.4.jar,/opt/bitnami/spark/jars/aws-java-sdk-bundle-1.12.262.jar',
        verbose=True,
        conf={
            'spark.hadoop.fs.s3a.access.key': MINIO_ACCESS_KEY_ID,
            'spark.hadoop.fs.s3a.secret.key': MINIO_SECRET_ACCESS_KEY,
            'spark.hadoop.fs.s3a.endpoint': MINIO_ENDPOINT_URL,
            'spark.hadoop.fs.s3a.impl': 'org.apache.hadoop.fs.s3a.S3AFileSystem',
            'spark.hadoop.fs.s3a.path.style.access': 'true'
        },
        application_args=[f"s3a://{TEMP_MINIO_BUCKET}/{TEMP_BUCKET_KEY}",
                          f"s3a://{TRANSFORM_MINIO_BUCKET}/{TRANSFORM_BUCKET_KEY}"]
    )

    load_postgres = PythonOperator(
        task_id='load_s3_to_postgres',
        python_callable=load_parquet_to_postgres,
        op_kwargs={
            'aws_conn_id': 'minio_s3',
            'bucket_name': TRANSFORM_MINIO_BUCKET,
            's3_key': TRANSFORM_BUCKET_KEY,
            'postgres_conn_id': 'postgres_default',
            'table_name': 'airport_info',
            'if_exists': 'replace'  # Optional: 'replace', 'append', or 'fail'
        }
    )


extract_task >> sensor_extract >> etl_transform >> load_postgres
