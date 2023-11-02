from src.ingestion_lambda.get_credentials import get_credentials
import os
import pytest
import boto3
from moto import mock_secretsmanager
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError
import json
import logging
logger = logging.getLogger()




@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


# 1. mock boto3 client.
# 2. check if the client gets instantiated as a secrets manager client.

# 3. mock the secrets manager client
# 4. check if the get_secret_value get invoked with secret_name param.

# 5. check if raises key error for missing keys

# 6. mock an empty secrets manager and check if
#    raises error when requesting for non existing secret

# 7.


@mock_secretsmanager
def test_ClientError_secret_that_does_not_exist(caplog):
    with caplog.at_level(logging.ERROR):
        get_credentials("not-a-real-secret")
        assert "Secret not-a-real-secret does not exist" in caplog.text
    

@mock_secretsmanager
def test_KeyError_with_missing_param(caplog):
    secret_string = {
        "host": "real host",
        "port": "definitely not a mock port",
        "password": "pa55word",
        "database": "database"
    }
    client = boto3.client("secretsmanager")
    client.create_secret(Name="Mock", SecretString=json.dumps(secret_string))
    with caplog.at_level(logging.ERROR):
        get_credentials("Mock")
        assert "Missing key 'user' in database credentials."


@mock_secretsmanager
def test_connection_params_look_like_expected():
    secret_string = {
        "host": "real host",
        "port": "definitely not a mock port",
        "user": "real human",
        "password": "pa55word",
        "database": "database"
    }
    client = boto3.client("secretsmanager")
    client.create_secret(Name="Mock", SecretString=json.dumps(secret_string))
    assert get_credentials("Mock") == {
        "host": "real host",
        "port": "definitely not a mock port",
        "user": "real human",
        "password": "pa55word",
        "database": "database"
    }