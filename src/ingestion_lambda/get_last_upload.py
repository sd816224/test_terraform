import boto3
from datetime import date
from datetime import timedelta
from datetime import datetime as dt


def get_last_upload(bucket_name):
    """retrieves the time the s3 bucket was modified

    returns a datetime object that can be used in a psql query

    Args:
        bucket name

    Raises:
        ???"""

    yesterday = date.today() - timedelta(days=1)
    year = yesterday.year
    month = yesterday.month
    day = yesterday.day

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    objs = [
        obj.last_modified.strftime("%Y:%m:%d:%H:%M:%S")
        for obj in bucket.objects.filter(Prefix=yesterday.strftime("%Y/%m/%d/"))
    ]
    print(objs)
