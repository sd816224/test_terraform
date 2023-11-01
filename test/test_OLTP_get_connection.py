import os
import logging
import pytest
from dotenv import load_dotenv
from pg8000.native import Connection, InterfaceError, DatabaseError
from src.ingestion_lambda.OLTP_get_connection import get_connection


logger = logging.getLogger('MyLogger')


def test_get_connection_returns_correct_log_when_successful_connection(caplog):
    '''
    This test should return the correct log in CloudWatch, when passed correct details
    Requirements:
        .env (using dotenv.load_dotenv module) file with credentials for accessing a database.
        credentials required are: user, host, port, database, and password.
    '''
    with caplog.at_level(logging.INFO):
        load_dotenv()
        user=os.environ['PGUSER']
        host=os.environ['PGHOST']
        port=os.environ['PGPORT']
        database=os.environ['DB']
        password=os.environ['PGPASSWORD']
        get_connection(user, host, database, port, password)
        assert('Connection to database Totesys has been established.' in caplog.text)


def test_get_connection_with_database_error():
    '''
    Testing for a DatabaseError. When passed incorrect details, should return DatabaseError.
    '''
    with pytest.raises(DatabaseError):
        load_dotenv()      
        user=os.environ['PGUSER']
        host=os.environ['PGHOST']
        port=os.environ['PGPORT']
        database=os.environ['DB']
        password=''
        get_connection(user, host, database, port, password)


def test_get_connection_with_unexpected_error():
    '''
    When passed an unexpected error, i.e. no password credentials passed, will return an error.
    '''
    with pytest.raises(Exception):
        load_dotenv()      
        user=os.environ['PGUSER']
        host=os.environ['PGHOST']
        port=os.environ['PGPORT']
        database=os.environ['DB']
        get_connection(user, host, database, port, password)

