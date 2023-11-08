from src.transformation_lambda.transformation_lambda import (
    read_s3_json,
    get_object_path,
    get_content_from_file,
)
from moto import mock_s3
import boto3
import json
from unittest.mock import patch


test_event = {
    "Records": [
        {
            "eventVersion": "2.1",
            "eventSource": "aws:s3",
            "awsRegion": "eu-west-2",
            "eventTime": "2023-11-03T11:11:19.251Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {"principalId": "testId"},
            "requestParameters": {"sourceIPAddress": "test_ip"},
            "responseElements": {
                "x-amz-request-id": "test_id",
                "x-amz-id-2": "test_id",
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "bucket_upload_something",
                "bucket": {
                    "name": "test_bucket_name",
                    "ownerIdentity": {"principalId": "testId"},
                    "arn": "test_arn",
                },
                "object": {
                    "key": "test_file.json",
                    "size": 0,
                    "eTag": "test_eTag",
                    "sequencer": "test_sequencer",
                },
            },
        }
    ]
}


def test_get_object_path_function_output_correct_bucket_and_file_name():
    bucket_name, file_name = get_object_path(test_event["Records"])
    assert bucket_name == "test_bucket_name"
    assert file_name == "test_file.json"


@mock_s3
def test_get_content_from_file_get_correct_content():
    fake_client = boto3.client("s3", region_name="us-east-1")
    example_dict = {"c1": 1, "c2": 2}
    json_data = json.dumps(example_dict)
    fake_client.create_bucket(Bucket="test_bucket")

    fake_client.put_object(
        Body=json_data, Bucket="test_bucket", Key="test_file.json"
    )  # noqa E501
    result_content = get_content_from_file(
        fake_client, "test_bucket", "test_file.json"
    )  # noqa E501
    assert result_content == '{"c1": 1, "c2": 2}'


@patch(
    "src.transformation_lambda.transformation_lambda.get_content_from_file",
    return_value='{"c1": 1, "c2": 2}',
)
def test_read_s3_json(get_content_from_file):
    assert read_s3_json(test_event) == {"c1": 1, "c2": 2}
