# import os
# import logging
# import pytest
# from dotenv import load_dotenv
# from pg8000 import DatabaseError, InterfaceError  # Connection,
# from src.ingestion_lambda.OLTP_get_connection import get_connection


# logger = logging.getLogger('MyLogger')
# logger.setLevel(logging.INFO)


# def test_get_connection_returns_correct_log_when_successful_con(caplog):
#     '''
#     This test should return the correct log in CloudWatch,
#     when passed correct details
#     Requirements:
#         .env (using dotenv.load_dotenv module) file consisting of
#         credentials for accessing a database.
#         credentials required are: user, host, port, database, and password.
#     '''
#     with caplog.at_level(logging.INFO):
#         load_dotenv()
#         database_credentials = {
#             'user': os.environ['PGUSER'],
#             'host': os.environ['PGHOST'],
#             'port': os.environ['PGPORT'],
#             'database': os.environ['DB'],
#             'password': os.environ['PGPASSWORD'],
#         }
#         get_connection(database_credentials)
#         assert ('Connection to database Totesys has been established.'
#                 in caplog.text)


# def test_get_connection_with_interface_error_no_user():
#     '''
#     Testing for a InterfaceError. When passed incorrect details,
#     should return InterfaceError message.
#     '''
#     with pytest.raises(InterfaceError):
#         load_dotenv()
#         database_credentials = {
#             'user': '',
#             'host': os.environ['PGHOST'],
#             'port': os.environ['PGPORT'],
#             'database': os.environ['DB'],
#             'password': os.environ['PGPASSWORD'],
#         }
#         get_connection(database_credentials)


# def test_get_connection_with_interface_error_no_host():
#     '''
#     Testing for a InterfaceError. When passed incorrect details,
#     should return InterfaceError message.
#     '''
#     with pytest.raises(InterfaceError):
#         load_dotenv()
#         database_credentials = {
#             'user': os.environ['PGUSER'],
#             'host': '',
#             'port': os.environ['PGPORT'],
#             'database': os.environ['DB'],
#             'password': os.environ['PGPASSWORD'],
#         }
#         get_connection(database_credentials)


# def test_for_interface_error_when_provided_incorrect_port():
#     '''
#     Testing for a InterfaceError. When passed incorrect port,
#     should return InterfaceError log, and will timeout after 5 seconds.
#     '''
#     with pytest.raises(InterfaceError):
#         load_dotenv()
#         database_credentials = {
#             'user': os.environ['PGUSER'],
#             'host': os.environ['PGHOST'],
#             'port': 1,
#             'database': os.environ['DB'],
#             'password': os.environ['PGPASSWORD'],
#         }
#         get_connection(database_credentials)


# def test_for_interface_error_when_provided_no_port():
#     '''
#     Testing for a InterfaceError. When passed incorrect port,
#     should return InterfaceError log, and will timeout after 5 seconds.
#     '''
#     with pytest.raises(InterfaceError):
#         load_dotenv()
#         database_credentials = {
#             'user': os.environ['PGUSER'],
#             'host': os.environ['PGHOST'],
#             'port': '',
#             'database': os.environ['DB'],
#             'password': os.environ['PGPASSWORD'],
#         }
#         get_connection(database_credentials)


# def test_get_connection_with_database_error_incorrect_database_name():
#     '''
#     Testing for a DatabaseError.
#     When passed incorrect details, should return DatabaseError.
#     '''
#     with pytest.raises(DatabaseError):
#         load_dotenv()
#         database_credentials = {
#             'user': os.environ['PGUSER'],
#             'host': os.environ['PGHOST'],
#             'port': os.environ['PGPORT'],
#             'database': 'wrong database name',
#             'password': os.environ['PGPASSWORD'],
#         }
#         get_connection(database_credentials)


# def test_get_connection_with_database_error_incorrect_password():
#     '''
#     Testing for a DatabaseError.
#     When passed incorrect details, should return DatabaseError.
#     '''
#     with pytest.raises(DatabaseError):
#         load_dotenv()
#         database_credentials = {
#             'user': os.environ['PGUSER'],
#             'host': os.environ['PGHOST'],
#             'port': os.environ['PGPORT'],
#             'database': os.environ['DB'],
#             'password': '',
#         }
#         get_connection(database_credentials)


# def test_get_connection_with_unexpected_error():
#     '''
#     When passed an unexpected error,
#     i.e. no password credentials passed, will return an error.
#     '''
#     with pytest.raises(Exception):
#         load_dotenv()
#         database_credentials = {
#             'user': os.environ['PGUSER'],
#             'host': os.environ['PGHOST'],
#             'port': os.environ['PGPORT'],
#             'database': os.environ['DB'],
#         }
#         get_connection(database_credentials)


# def test_get_connection_with_key_error():
#     '''
#     Testing for a key_error.
#     When passed incorrect key, should return exception log message.
#     '''
#     with pytest.raises(Exception):
#         load_dotenv()
#         database_credentials = {
#             'user': os.environ['PGUSER'],
#             'host': os.environ['PGHOST'],
#             'port': os.environ['PGPORT'],
#             'database': os.environ['DB'],
#             'incorrect_key': os.environ['PASSWORD'],
#         }
#         get_connection(database_credentials)
