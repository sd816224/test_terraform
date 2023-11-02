from unittest.mock import Mock
import json
import pytest
import logging
from src.ingestion_lambda.get_data import get_data


logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


def mock_run(str, date='ss'):
    '''
    Mock table data
    '''
    if "SELECT table_name" in str:
        return [['table_a'], ['table_b'], ['_prisma_migrations']]
    elif "SELECT * FROM table_a" in str:
        return [[1, 2, 3], [11, 22, 33]]
    elif "SELECT * FROM table_b" in str:
        return [[10, 20, 30], [110, 220, 330]]
    elif "SELECT column_name" in str:
        return [['c1'], ['c2'], ['c3']]


def mock_run_with_incorrect_columns(str, date='ss'):
    '''
    Mock table data
    '''
    if "SELECT table_name FROM information_schema.tables " in str:
        return [['table_a'], ['table_b'], ['_prisma_migrations']]
    elif "SELECT * FROM table_a" in str:
        return [[1, 2, 3], [11, 22, 33]]
    elif "SELECT * FROM table_b" in str:
        return [[10, 20, 30], [110, 220, 330]]
    elif "SELECT column_name FROM information_schema.columns" in str:
        return [['c1'], ['c2']]


def test_get_data_get_all_table_names_with_multiple_table_and_column_names():
    '''
    This test uses the mock data as the connection, and tests the correct
    response when passed a set of test database tables, column names, and data.
    '''
    expected_updated_content = {
        "table_a": [
            {
                "c1": 1,
                "c2": 2,
                "c3": 3
            },
            {
                "c1": 11,
                "c2": 22,
                "c3": 33
            }
        ],
        "table_b": [
            {
                "c1": 10,
                "c2": 20,
                "c3": 30
            },
            {
                "c1": 110,
                "c2": 220,
                "c3": 330
            }
        ]
    }
    updated_json = json.dumps(expected_updated_content,
                              indent=4, sort_keys=True, default=str)
    conn_mock = Mock()
    conn_mock.run.side_effect = mock_run
    assert get_data(conn_mock) == updated_json


def test_get_data_returns_correct_log_when_successful_connection(caplog):
    '''
    When get_data util is successful, test to check the correct log is passed
    in CloudWatch.
    '''
    # logger.info('Connection to database Totesys has been established.')
    with caplog.at_level(logging.INFO):
        conn_mock = Mock()
        conn_mock.run.side_effect = mock_run
        get_data(conn_mock)
        assert ('Updated JSON content has been retrieved.' in caplog.text)


def test_get_data_will_return_error_message_in_logs():
    '''
    This test uses the mock data as the connection, and tests the correct
    response when passed a set of test database tables, column names, and data.
    '''
    with pytest.raises(Exception):
        conn_mock = Mock()
        conn_mock.run.side_effect = mock_run_with_incorrect_columns
        get_data(conn_mock)
