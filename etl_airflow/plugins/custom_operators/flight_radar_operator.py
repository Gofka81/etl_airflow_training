import os
import requests
import boto3
import io
import json

from airflow.models import BaseOperator
from airflow.exceptions import AirflowException

MINIO_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL")
MINIO_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY_ID")
MINIO_SECRET_ACCESS_KEY = os.getenv("MINIO_SECRET_ACCESS_KEY")
FLIGHT_RADAR_URL = os.getenv("FLIGHT_RADAR_URL")


class FlightRadarOperator(BaseOperator):
    def __init__(self, route: str, src_bucket, **kwargs):
        self.route = route
        self.src_bucket = src_bucket
        super().__init__(**kwargs)

    def execute(self, context):
        api_request = f'{FLIGHT_RADAR_URL}/{self.route}'

        try:
            data = self.extract_data_from_api(api_request)
            self.store_data_to_s3(data, context)
        except Exception as e:
            raise AirflowException(e)

    @staticmethod
    def extract_data_from_api(api_request: str):
        response = requests.get(api_request)
        response.raise_for_status()
        data = response.json()
        count = 0
        for i in data:
            count += len(i)
        print(f"Total flights fetched {count}")
        return data

    def store_data_to_s3(self, data: list, context):
        formatted_date = context['logical_date'].strftime("%m-%d-%Y_%H:%M:%S")
        dag_name = context["dag"].dag_id
        try:
            s3_client = boto3.client(
                's3',
                endpoint_url=MINIO_ENDPOINT_URL,
                aws_access_key_id=MINIO_ACCESS_KEY_ID,
                aws_secret_access_key=MINIO_SECRET_ACCESS_KEY,
            )

            # Store data in S3
            data_str = json.dumps(data)
            data_bytes = io.BytesIO(data_str.encode('utf-8'))
            object_name = f'{dag_name}/timestamp={formatted_date}/{self.route}.json'

            s3_client.upload_fileobj(
                data_bytes,
                self.src_bucket,
                object_name,
                ExtraArgs={'ContentType': 'application/json'}
            )
            print(f"Data successfully stored in S3 bucket '{self.src_bucket}' with object name '{object_name}'")
        except Exception as e:
            raise AirflowException(e)
