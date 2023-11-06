from src.transformation_lambda.format_dim_currency import format_dim_currency
import pytest
import logging


test_currency = {
    "currency": [
        {
            "currency_id": 1,
            "currency_code": "GBP",
            "created_at": "2022-11-03T14:20:49.962",
            "last_updated": "2022-11-03T14:20:49.962"
        },
        {
            "currency_id": 2, "currency_code": "USD",
            "created_at": "2022-11-03T14:20:49.962",
            "last_updated": "2022-11-03T14:20:49.962"
        },
        {
            "currency_id": 3,
            "currency_code": "EUR",
            "created_at": "2022-11-03T14:20:49.962",
            "last_updated": "2022-11-03T14:20:49.962"
        }
    ]
}


def test_output_rows_has_correct_key_names():
    result = format_dim_currency(test_currency)
    for row in result:
        assert 'currency_id' in row
        assert 'currency_code' in row
        assert 'currency_name' in row
        assert len(row) == 3


def test_correct_output():
    result = format_dim_currency(test_currency)
    assert len(result) == 3
    assert {'currency_id': 1,
            'currency_code': 'GBP',
            'currency_name': 'Pound Sterling'} in result

    assert {'currency_id': 2,
            'currency_code': 'USD',
            'currency_name': 'United States dollar'} in result
    assert {'currency_id': 3,
            'currency_code': 'EUR',
            'currency_name': 'Euros'} in result


def test_KeyError_happend_when_wrong_table_name(caplog):
    wrong_table = {'anything': test_currency['currency']}
    with caplog.at_level(logging.ERROR):
        format_dim_currency(wrong_table)
        assert 'Error retrieving data' in caplog.text


def test_RuntimeError_happend_when_wrong_input():
    with pytest.raises(RuntimeError):
        format_dim_currency(5)
