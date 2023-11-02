import boto3
from datetime import datetime as dt
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)


def get_last_upload(bucket_name):
    """retrieves the time the s3 bucket was modified

    returns a datetime object that can be used in a psql query
    if no last update file exists it returns a default datetime object

    Args:
        bucket name

    Raises:
        clientError"""

    client = boto3.client("s3")

    try:
        response = client.get_object(Bucket=bucket_name, Key="last_update.txt")
        datetime_string = response["Body"].read().decode("utf-8")
        datetime_object = dt.strptime(datetime_string, "%Y:%m:%d:%H:%M:%S")

        return datetime_object
    except ClientError as e:
        message = e.response["Error"]["Message"]
        if message == "The specified key does not exist.":
            dt_object = dt.strptime("2020:1:1:00:00:00", "%Y:%m:%d:%H:%M:%S")
            logger.info("default datetime object returned")
            return dt_object
        else:
            logger.error(e.response["Error"]["Message"])
    except Exception as e:
        logger.error(f"An unexpected error occured {e}")
