import boto3
import logging
from datetime import datetime as dt
from botocore.exceptions import ClientError
import json

logging.basicConfig()
logger = logging.getLogger("ingestion_lambda")
logger.setLevel(logging.INFO)


def write_file(bucket_name, json_data):
    """handles creation of new data file in s3 bucket.

    Saves the json file with a time stamp to organise structure of s3 buckets.

    Args:
        s3 bucket name
        json data from the get_data util

    Raises:
        ClientError: Issue occured regarding putting object into s3 bucket.
    """

    client = boto3.client("s3")
    date = dt.now()
    year = date.year
    month = date.month
    day = date.day
    time = date.strftime("%H%M%S")

    file_name = f"{year}/{month}/{day}/data-{time}.json"

    try:
        if json_data is None:
            raise Exception("No JSON data provided")

        response = client.put_object(
            Body=json.dumps(json_data), Bucket=bucket_name, Key=file_name
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logger.info(f"Success. File {file_name} saved.")

    except ClientError as e:
        logger.error(f" {e.response['Error']['Message']}")
    except Exception as e:
        logger.error(e)
