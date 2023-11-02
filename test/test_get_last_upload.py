from src.ingestion_lambda.get_last_upload import get_last_upload
from moto import mock_s3
import pytest
import os
import boto3
from pprint import pprint
import time


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@mock_s3
class TestGetLastUpload:
    def test_returns_date_of_most_recent_modification(self):
        client = boto3.client("s3")
        client.create_bucket(
            Bucket="TestBucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        client.put_object(Body="stuff", Key="2023/11/1/stuff1", Bucket="TestBucket")
        time.sleep(2)
        client.put_object(Body="stuff", Key="2023/11/1/stuff2", Bucket="TestBucket")
        time.sleep(2)
        client.put_object(Body="stuff", Key="2023/10/31/stuff3", Bucket="TestBucket")

        get_last_upload("TestBucket")
