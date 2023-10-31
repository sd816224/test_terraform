import os
from src.utils.OLTP_get_connection import get_connection


def test_get_connection_returns_correct_print(capsys):
    '''
    Testing get_connection function. Function, if successful, will print:
    "Connection to database Totesys has been established."
    '''
    get_connection()
    captured = capsys.readouterr()
    all_outputs=captured.out.split('\n')
    last_outputs=all_outputs[0]
    expected = 'Connection to database Totesys has been established.'
    print(f'Result is: {last_outputs}')
    assert last_outputs == expected
