import logging
import boto3
from botocore.exceptions import ClientError
import json

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


def read_s3_json(event, context):
    """Handles S3 PutObject event
    read recent stored json file
    and convert to dictionary

    On receipt of a PutObject event, checks that the file type is txt and
    then logs the contents.

    Args:
        event:
            a valid S3 PutObject event
        context:
            a valid AWS lambda Python context object - see
            https://docs.aws.amazon.com/lambda/latest/dg/python-context.html

    Return:
        dictionary formatted json content.

    Raises:
        RuntimeError: An unexpected error occurred in execution. Other errors
        result in an informative log message.
    """

    try:
        s3_bucket_name, s3_object_name = get_object_path(event['Records'])
        logger.info(f'Bucket is {s3_bucket_name}')
        logger.info(f'Object key is {s3_object_name}')

        if s3_object_name[-4:] != 'json':
            raise InvalidFileTypeError

        s3 = boto3.client('s3')
        content = get_content_from_file(s3, s3_bucket_name, s3_object_name)
        dict_format_conetent = json.loads(content)
        logger.info('File contents:::::::::::::::::::::')
        logger.info(f'{content}')
        return dict_format_conetent
    except KeyError as k:
        logger.error(f'Error retrieving data, {k}')
    except ClientError as c:
        if c.response['Error']['Code'] == 'NoSuchKey':
            logger.error(f'No object found - {s3_object_name}')
        elif c.response['Error']['Code'] == 'NoSuchBucket':
            logger.error(f'No such bucket - {s3_bucket_name}')
        else:
            raise
    except UnicodeError:
        logger.error(f'File {s3_object_name} is not a valid text file')
    except InvalidFileTypeError:
        logger.error(f'File {s3_object_name} is not a valid text file')
    except Exception as e:
        logger.error(e)
        raise RuntimeError


def get_object_path(records):
    """Extracts bucket and object references from Records field of event."""
    return records[0]['s3']['bucket']['name'], \
        records[0]['s3']['object']['key']


def get_content_from_file(client, bucket, object_key):
    """Reads text from specified file in S3."""
    data = client.get_object(Bucket=bucket, Key=object_key)
    contents = data['Body'].read()
    return contents.decode('utf-8')


class InvalidFileTypeError(Exception):
    """Traps error where file type is not json."""
    pass
