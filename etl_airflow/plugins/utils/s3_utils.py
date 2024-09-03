import io
import pandas as pd
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook


def load_parquet_to_postgres(**kwargs):
    # Extract parameters from kwargs
    aws_conn_id = kwargs['aws_conn_id']
    bucket_name = kwargs['bucket_name']
    s3_key = kwargs['s3_key']
    postgres_conn_id = kwargs['postgres_conn_id']
    table_name = kwargs['table_name']
    if_exists = kwargs.get('if_exists', 'replace')  # Default to 'replace' if not provided

    # S3 connection
    s3_hook = S3Hook(aws_conn_id=aws_conn_id)

    keys = s3_hook.list_keys(bucket_name=bucket_name, prefix=s3_key)

    # Filter to only parquet files if needed
    parquet_keys = [key for key in keys if key.endswith('.parquet')]

    dataframes = []

    print(parquet_keys)

    # Loop through all parquet files and read them into a dataframe
    for key in parquet_keys:
        # Read the object from S3
        obj = s3_hook.get_key(key, bucket_name=bucket_name)

        # Read the parquet file into a Pandas DataFrame
        df = pd.read_parquet(io.BytesIO(obj.get()['Body'].read()))
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    # Postgres connection
    postgres_hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    engine = postgres_hook.get_sqlalchemy_engine()

    # Load the DataFrame into PostgreSQL
    combined_df.to_sql(table_name, engine, if_exists=if_exists, index=False)


def check_and_delete_s3_file(**kwargs):
    aws_conn_id = kwargs['aws_conn_id']
    bucket_name = kwargs['bucket_name']
    s3_key = kwargs['s3_key']
    s3_hook = S3Hook(aws_conn_id=aws_conn_id)
    for file in s3_hook.list_keys(bucket_name=bucket_name, prefix=s3_key):
        s3_hook.delete_objects(bucket=bucket_name, keys=file)
        print(f'Deleted: {file}')
