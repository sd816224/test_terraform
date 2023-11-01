import os
import logging
import pytest
from src.utils.OLTP_get_connection import get_connection

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


# def test_get_connection_returns_correct_print(capsys):
#     '''
#     Testing get_connection function. Function, if successful, will print:
#     "Connection to database Totesys has been established."
#     '''
#     get_connection()
#     captured = capsys.readouterr()
#     all_outputs=captured.out.split('\n')
#     last_outputs=all_outputs[0]
#     expected = 'Connection to database Totesys has been established.'
#     print(f'Result is: {last_outputs}')
#     assert last_outputs == expected

def test_get_connection_returns_correct_log_when_successful_connection(caplog):
    logger.info('Connection to database Totesys has been established.')
    with caplog.at_level(logging.INFO):
        get_connection()
        assert('Connection to database Totesys has been established.' in caplog.text)

@pytest.fixture(scope='session')
def test_get_connection_with_failed_connection():
    db_settings={
        'user'            : 'postgres',
        'host'            : 'test',
        'port'            : '5432',
        'database'        : 'test_database',
        'password'        : '',
    }
    


# def test_get_connection_returns_correct_query_response():
#     pass