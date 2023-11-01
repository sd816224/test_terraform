from src.ingestion_lambda.get_credentials import get_credendials
import os
import pytest
import moto
from moto import mock_secretsmanager
from unittest.mock import Mock, patch


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


def test():
    pass
