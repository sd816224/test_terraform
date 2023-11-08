import boto3
import logging
import json
import pandas as pd
from datetime import datetime as dt
from botocore.exceptions import ClientError
from pg8000 import Connection, DatabaseError, InterfaceError

logging.basicConfig()
logger = logging.getLogger("ingestion_lambda")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    invocation_time = dt.now()
    bucket_name = (
        #change name of your bucket!!!!!!!!!!!!!!!!!!!!!
        "hange name of your bucket!!!!!!!!!!!!!!!!!!!!!"  # noqa E501
    )
    secret_name = "totesys-production"

    try:
        credentials = get_credentials(secret_name)

        connection = get_connection(credentials)

        last_upload = get_last_upload(bucket_name)

        json_data = get_data(connection, last_upload)

        if json_data != {}:
            write_file(bucket_name, json_data, invocation_time)
        else:
            logger.info("No new updates to write to file")
    except Exception as e:
        logger.error(e)


"""util functions"""


def get_credentials(secret_name):
    """
    Gets credentials from the AWS secrets manager.

    Parameters
    ----------
    secret_name: str, required
        The name of the database credentials secret the lambda is trying to
        connect to.

    options:
        "totesys-production"
        "totesys-warehouse"

    Raises
    ------
    ClientError
        If the secret name is not found in the secrets manager.
        If there is an unexpected error connecting to the secrets manager.
    KeyError
        If the credentials object has a missing key.

    Returns
    ------
    dictionary
        a json-like object that contains the database connection credentials
        that can be accessed using the following keys:
        host, port, user, password, database

    """

    try:
        client = boto3.client("secretsmanager", region_name="eu-west-2")
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response["SecretString"])

        connection_params = {
            "host": secret["host"],
            "port": secret["port"],
            "user": secret["user"],
            "password": secret["password"],
            "database": secret["database"],
        }
        logger.info("connection parameters returned")
        return connection_params

    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.error(f"Secret {secret_name} does not exist.")
        else:
            logger.error(f"Error accessing database secret {secret_name}: {e}")
    except KeyError as e:
        logger.error(f"Missing key {e} in database credentials.")


def get_connection(database_credentials):
    """
    Gets connections to the OLTP database - Totesys.


    Parameters
    ----------
    database_credentials (from the get_credentials util),
    which is a dictionary consisting of:
        user
        host
        database
        port
        password

    Raises
    ------
    DatabaseError: Will return an error message showing what is missing.
        i.e. if the password is wrong, the error message will state password
        authentication has failed.
    InterfaceError:

    Returns
    -------
    A successful pg8000 connection object will be returned.
    """
    try:
        user = database_credentials["user"]
        host = database_credentials["host"]
        database = database_credentials["database"]
        port = database_credentials["port"]
        password = database_credentials["password"]
        conn = Connection(user, host, database, port, password, timeout=5)
        logger.info("Connection to database Totesys has been established.")
        return conn
    except DatabaseError as db:
        logger.error(f"pg8000 - an error has occurred: {db.args[0]['M']}")
        raise db
    except InterfaceError as ie:
        logger.error(f'pg8000 - an error has occurred: \n"{ie}"')
        raise ie
    except Exception as exc:
        logger.error(
            "An error has occurred when \
            attempting to connect to the database."
        )
        raise exc


def get_last_upload(bucket_name):
    """retrieves the time the s3 bucket was modified

    returns a datetime object that can be used in a psql query
    if no last update file exists it returns a default datetime object

    Args:
    -----
        bucket name

    Raises:
    -------
        clientError"""

    client = boto3.client("s3")

    try:
        response = client.get_object(Bucket=bucket_name, Key="last_update.txt")
        datetime_string = response["Body"].read().decode("utf-8")
        datetime_object = dt.strptime(datetime_string, "%Y:%m:%d:%H:%M:%S")
        logger.info("last updated datetime object returned")
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
        logger.error(f"An unexpected error occurred {e}")


def get_data(conn, last_upload):
    """
    Gets data from the connected database from last_upload


    Parameters
    ----------
    conn: database connection instance
        type: pg8000 connect object
    last_upload: the timestamp of the last fetched data file
        type: datetime object

    Returns
    -------
    JSON formatted updated content
    """
    # have checked that all created_at=last_updated in sales_order,
    # need to check other tables that we can cross check if or statement work

    # query to get all table names from database
    try:
        updated_content = {}
        table_names = conn.run(
            """
                            SELECT table_name
                            FROM information_schema.tables
                            WHERE table_schema = 'public';
                            """
        )
        list_table_names = list(table_names)
        list_table_names.append(["all_addresses"])
        list_table_names.remove(["_prisma_migrations"])
        for table in list_table_names:
            if table[0] == "department":
                content = conn.run(
                    f"""
                                    SELECT * FROM {table[0]}
                                    """
                )
            elif table[0] == "all_addresses":
                content = conn.run(
                    """
                                    SELECT * FROM address
                                    """
                )
            # get updated content from other tables
            else:
                content = conn.run(
                    f"""
                                    SELECT * FROM {table[0]}
                                    WHERE (last_updated > :date)
                                    """,
                    date={last_upload.strftime("%Y-%m-%dT%H:%M:%S")},
                )

            # get all column names from the table
            if table[0] == "all_addresses":
                columns = conn.run(
                    """
                                    SELECT column_name
                                    FROM information_schema.columns
                                    WHERE table_schema='public'
                                    AND table_name= 'address'
                                    """
                )
            else:
                columns = conn.run(
                    f"""
                                    SELECT column_name
                                    FROM information_schema.columns
                                    WHERE table_schema='public'
                                    AND table_name= '{table[0]}'
                                    """
                )
            column_names = [name[0] for name in columns]
            # integrate column names and conn to the dataframe
            df = pd.DataFrame(content, columns=column_names)
            json_formatted = df.to_json(orient="records", date_format="iso")
            back_to_list = json.loads(json_formatted)
            if len(back_to_list) != 0:
                updated_content[table[0]] = back_to_list
        conn.close()
        if list(updated_content.keys()) == ["department", "all_addresses"]:
            updated_content = {}

        logger.info("Updated JSON content has been retrieved.")
        return updated_content
    except Exception as exc:
        logger.error(exc)
        raise exc


def write_file(bucket_name, json_data, timestamp=dt(2020, 1, 1, 0, 0, 0)):
    """handles creation of new data file in s3 bucket.

    Saves the json file with a time stamp to organise structure of s3 buckets.
    Overwrites a last_updated file with the time the handler was invoked.

    Args:
    -----
        s3 bucket name
        json data from the get_data util (string)
        datetime object timestamp from the lambda handler when it is invoked

    Raises:
    -------
        ClientError: Issue occurred regarding putting object into s3 bucket.
    """

    client = boto3.client("s3")
    date = dt.now()
    year = date.year
    month = date.month
    day = date.day
    time = date.strftime("%H%M%S")

    last_successful_timestamp = timestamp.strftime("%Y:%m:%d:%H:%M:%S")

    try:
        if json_data is None:
            raise Exception("No JSON data provided")

        if not isinstance(json_data, dict):
            raise Exception("Updated data type invalid. Dict expected.")

        for table in json_data:
            if table != "all_addresses":
                file_name = f"{table}/{year}/{month}/{day}/data-{time}.json"

                if table == "staff":
                    response = client.put_object(
                        Body=json.dumps(
                            {
                                table: json_data[table],
                                "department": json_data["department"],
                            }  # noqa E501
                        ),
                        Bucket=bucket_name,
                        Key=file_name,
                    )  # noqa E501
                    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        logger.info(f"Success. File {file_name} saved.")

                elif table == "counterparty":
                    response = client.put_object(
                        Body=json.dumps(
                            {
                                table: json_data[table],
                                "address": json_data["all_addresses"],
                            }  # noqa E501
                        ),
                        Bucket=bucket_name,
                        Key=file_name,
                    )  # noqa E501
                    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        logger.info(f"Success. File {file_name} saved.")

                else:
                    response = client.put_object(
                        Body=json.dumps({table: json_data[table]}),
                        Bucket=bucket_name,
                        Key=file_name,
                    )  # noqa E501
                    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        logger.info(f"Success. File {file_name} saved.")

        datefileresponse = client.put_object(
            Body=last_successful_timestamp,
            Bucket=bucket_name,
            Key="last_update.txt",
        )
        if datefileresponse["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logger.info("Success. last_update.txt overwritten")
    except KeyError as e:
        logger.error(f" {e.response['Error']['Message']}")
    except ClientError as e:
        logger.error(f" {e.response['Error']['Message']}")
    except Exception as e:
        logger.error(e)
