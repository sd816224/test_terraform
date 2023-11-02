from src.ingestion_lambda.get_last_upload import get_last_upload
from moto import mock_s3
import pytest
import os
import boto3
from pprint import pprint
from datetime import datetime as dt
import logging


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
        client.put_object(
            Body="2023:11:2:00:00:00", Key="last_update.txt", Bucket="TestBucket"
        )
        result = get_last_upload("TestBucket")
        assert result == dt(2023, 11, 2, 0, 0, 0)

    def test_returns_default_datetime_if_no_last_update_exists(self):
        client = boto3.client("s3")
        client.create_bucket(
            Bucket="TestBucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        client.put_object(
            Body="2023:11:2:00:00:00", Key="not_a_file.txt", Bucket="TestBucket"
        )
        result = get_last_upload("TestBucket")
        assert result == dt(2020, 1, 1, 0, 0, 0)

    def test_logs_when_default_datetime_is_returned(self, caplog):
        with caplog.at_level(logging.INFO):
            client = boto3.client("s3")
            client.create_bucket(
                Bucket="TestBucket",
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
            client.put_object(
                Body="2023:11:2:00:00:00", Key="not_a_file.txt", Bucket="TestBucket"
            )
            get_last_upload("TestBucket")

            assert "default datetime object returned" in caplog.text

    def test_logs_client_error_when_invalid_bucket_name(self, caplog):
        with caplog.at_level(logging.INFO):
            client = boto3.client("s3")
            client.create_bucket(
                Bucket="TestBucket",
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
            client.put_object(
                Body="2023:11:2:00:00:00", Key="not_a_file.txt", Bucket="TestBucket"
            )
            get_last_upload("NotABucket")

            assert "The specified bucket does not exist" in caplog.text
