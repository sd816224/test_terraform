import boto3
import io
import logging
import pandas as pd
import datetime as dt
from botocore.exceptions import ClientError


logging.basicConfig()
logger = logging.getLogger("transformation_lambda")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    bucket_name = "nc-de-project-transformed-data-20231102173127140100000001"

    # 1. read_s3_json(event)
    # 2. select a function to do the formatting based on table_name
    # 3. turn formatted data into data frame and then parquet as temp
    # 4. Write to s3

    formatting_functions = {
        "staff": format_dim_staff,
        "design": format_dim_design,
        "curency": format_dim_currency,
        "counterparty": format_dim_counterparty,
        "???": format_dim_location,
        "sales_order": format_dim_date,
        "sales_order??": format_fact_sales_order,
    }

    # get table name here first or from read_s3_json output and then get table_name?

    try:
        if table_name in formatting_functions:
            data = read_s3_json(event)
            formatted_data = formatting_functions[table_name](data)
            parquet_buffer = create_parquet_buffer(formatted_data)
            write_file_to_s3(bucket_name, table_name, parquet_buffer)
        else:
            logger.info("Table name not found in formatting_functions.")
    except Exception as e:
        logger.error(f"VERY BAD EXCEPTION! HURHUR!: {e}")


def read_s3_json(event):
    pass


def create_parquet_buffer(formatted_data):
    """
    Write table data as parquet to an
    in-memory buffer before uploading it to s3
    """
    # create a dataframe
    df = pd.DataFrame(formatted_data)
    # create in-memory binary stream
    parquet_buffer = io.BytesIO()
    # write parquet to the stream
    df.to_parquet(parquet_buffer)
    # re-set pointer to the beggining of the buffer if .read() is used
    # parquet_buffer.seek(0)
    return parquet_buffer


def write_file_to_s3(bucket_name, table_name, parquet_buffer):
    client = boto3.client("s3")
    date = dt.now()
    year = date.year
    month = date.month
    day = date.day
    time = date.strftime("%H%M%S")

    file_name = f"{table_name}/{year}/{month}/{day}/data-{time}.parquet"

    try:
        response = client.put_object(
            Body=parquet_buffer.getvalue(), Bucket=bucket_name, Key=file_name
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logger.info(f"Success. File {file_name} saved.")

    except KeyError as e:
        logger.error(f" {e.response['Error']['Message']}")
    except ClientError as e:
        logger.error(f" {e.response['Error']['Message']}")
    except Exception as e:
        logger.error(e)


def format_dim_staff():
    pass


def format_dim_design():
    pass


def format_dim_currency():
    pass


def format_dim_counterparty():
    pass


def format_dim_location():
    pass


def format_dim_date():
    pass


def format_fact_sales_order():
    pass
