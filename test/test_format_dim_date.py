from src.transformation_lambda.format_dim_date import format_dim_date
import datetime
import pytest
import logging

test_table = {
    "sales_order": [
        {
            "agreed_delivery_date": "2023-11-02",
            "agreed_delivery_location_id": 10,
            "agreed_payment_date": "2023-11-03",
            "counterparty_id": 6,
            "created_at": "2023-10-30T08:27:09.957",
            "currency_id": 3,
            "design_id": 112,
            "last_updated": "2023-10-30T08:27:09.957",
            "sales_order_id": 4981,
            "staff_id": 5,
            "unit_price": 2.64,
            "units_sold": 26768
        },
        {
            "agreed_delivery_date": "2023-11-02",
            "agreed_delivery_location_id": 6,
            "agreed_payment_date": "2023-11-02",
            "counterparty_id": 5,
            "created_at": "2023-10-30T09:51:09.719",
            "currency_id": 3,
            "design_id": 131,
            "last_updated": "2023-10-30T09:51:09.719",
            "sales_order_id": 4982,
            "staff_id": 15,
            "unit_price": 3.87,
            "units_sold": 66274
        },
        {
            "agreed_delivery_date": "2023-11-01",
            "agreed_delivery_location_id": 17,
            "agreed_payment_date": "2023-11-05",
            "counterparty_id": 17,
            "created_at": "2023-11-01T16:06:09.791",
            "currency_id": 3,
            "design_id": 147,
            "last_updated": "2023-11-01T16:06:09.791",
            "sales_order_id": 5035,
            "staff_id": 1,
            "unit_price": 2.59,
            "units_sold": 65588
        }
    ]
}


def test_output_rows_has_correct_key_names():
    result = format_dim_date(test_table)
    for date in result:
        assert 'date_id' in date
        assert 'day' in date
        assert 'day_name' in date
        assert 'day_of_week' in date
        assert 'month' in date
        assert 'month_name' in date
        assert 'quarter' in date
        assert 'year' in date


def test_correct_output():
    result = format_dim_date(test_table)
    assert len(result) == 5
    assert {'date_id': datetime.datetime(2023, 11, 2, 0, 0),
            'day': 2,
            'day_name': 'Thursday',
            'day_of_week': 3,
            'month': 11,
            'month_name': 'November',
            'quarter': 3,
            'year': 2023} in result

    assert {'date_id': datetime.datetime(2023, 11, 3, 0, 0),
            'day': 3,
            'day_name': 'Friday',
            'day_of_week': 4,
            'month': 11,
            'month_name': 'November',
            'quarter': 3,
            'year': 2023} in result
    assert {'date_id': datetime.datetime(2023, 10, 30, 0, 0),
            'day': 30,
            'day_name': 'Monday',
            'day_of_week': 0,
            'month': 10,
            'month_name': 'October',
            'quarter': 3,
            'year': 2023} in result
    assert {'date_id': datetime.datetime(2023, 11, 1, 0, 0),
            'day': 1,
            'day_name': 'Wednesday',
            'day_of_week': 2,
            'month': 11,
            'month_name': 'November',
            'quarter': 3,
            'year': 2023} in result
    assert {'date_id': datetime.datetime(2023, 11, 5, 0, 0),
            'day': 5,
            'day_name': 'Sunday',
            'day_of_week': 6,
            'month': 11,
            'month_name': 'November',
            'quarter': 3,
            'year': 2023} in result


def test_KeyError_happend_when_wrong_table_name(caplog):
    wrong_table = {'staff': test_table['sales_order']}
    with caplog.at_level(logging.ERROR):
        format_dim_date(wrong_table)
        assert 'Error retrieving data' in caplog.text


def test_RuntimeError_happend_when_wrong_input():
    with pytest.raises(RuntimeError):
        format_dim_date(5)
