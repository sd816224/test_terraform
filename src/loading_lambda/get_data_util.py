import logging
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from io import BytesIO


logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)


def get_parquet(bucket_name, file_name):
    """
    This function extracts the parquet file
    which invoked the lambda and returns
    the values of the rows in a list of tuples.

    Parameters
    ----------
        bucket_name:
            the name of the bucket containing the parquet files.
        file_name:
            the name of the file triggering the lambda.

    Returns
    -------
        a list of tuples representing the values of each row.

     
    """
    client = boto3.client("s3")
    try:
        response = client.get_object(Bucket=bucket_name, Key=file_name)
        restored_df = pd.read_parquet(BytesIO(response["Body"].read()))
        values = restored_df.values.tolist()

        list_of_tuples = [tuple(list) for list in values]

        return list_of_tuples
    except ClientError as e:
        logger.error(e.response["Error"]["Message"])
    except Exception as e:
        logger.error(f"An unexpected error occurred {e}")
