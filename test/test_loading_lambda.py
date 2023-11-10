from src.loading_lambda.loading_lambda import lambda_handler
from unittest.mock import patch
from moto import mock_s3
import subprocess
import logging
import pg8000
import time
import boto3
import pytest
import os

# from moto import mock_s3
# import time_machine
# from datetime import datetime as dt

logger = logging.getLogger("TestLogger")
logger.setLevel(logging.INFO)


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


# 1. initdb psql container with wh schema. (docker-compose-wh.yaml)
# 2. mock get_credentials for the psql container.
# 3. mock s3 with parquet already uploaded (fixture)
# 4. mock event object with correct bucket name and parquet file path.

# fixture and path order in test function?
# move file upload to s3 fixture?


@pytest.fixture(scope="module")
def pg_container_fixture():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    compose_path = os.path.join(test_dir, "docker-compose-dw.yaml")
    subprocess.run(
        ["docker", "compose", "-f", compose_path, "up", "-d"], check=False
    )  # noqa: E501
    try:
        max_attempts = 5
        for _ in range(max_attempts):
            result = subprocess.run(
                [
                    "docker",
                    "exec",
                    "postgres-dw",
                    "pg_isready",
                    "-h",
                    "localhost",
                    "-U",
                    "testdb",
                ],
                stdout=subprocess.PIPE,
                check=False,
            )
            if result.returncode == 0:
                break
            time.sleep(2)
        else:
            raise TimeoutError(
                """PostgreSQL container is not responding,
                cancelling fixture setup."""
            )
        yield
    finally:
        subprocess.run(
            ["docker", "compose", "-f", compose_path, "down"], check=False
        )  # noqa: E501


@pytest.fixture
def s3_fixture():
    with mock_s3():
        s3_client = boto3.client("s3")
        bucket_name = "test-transformed-data-bucket"
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )  # noqa: E501
        yield s3_client, bucket_name


@patch(
    "src.loading_lambda.loading_lambda.get_credentials",
    return_value={
        "user": "testuser",
        "password": "testpass",
        "database": "testdb",
        "host": "localhost",
        "port": 5433,
    },
)
def test_loading_lambda(get_credentials, pg_container_fixture, s3_fixture):
    s3_client, s3_bucket = s3_fixture

    with open("test/mock_parquet/data-144511.parquet", "rb") as file:
        s3_client.put_object(
            Body=file.read(),
            Bucket=s3_bucket,
            Key="dim_staff/dim_staff.parquet",  # noqa E501
        )

    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": s3_bucket},
                    "object": {"key": "dim_staff/dim_staff.parquet"},
                }
            }
        ]
    }
    lambda_handler(event, "context")

    conn = pg8000.connect(
        user="testuser",
        password="testpass",
        host="localhost",
        port=5433,
        database="testdb",
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * from dim_staff limit 1;")
    result = cursor.fetchone()  # [0]
    assert result == (
        [
            1,
            "Jeremie",
            "Franey",
            "Purchasing",
            "Manchester",
            "jeremie.franey@terrifictotes.com",
        ]
    )
