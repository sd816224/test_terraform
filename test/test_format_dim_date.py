from src.transformation_lambda.format_dim_date import format_dim_date
import pytest
import logging

test_table = {
    "sales_order": [
        {
            "sales_order_id": 4981,
            "created_at": "2023-10-30T08:27:09.957",
            "last_updated": "2023-10-30T08:27:09.957",
            "design_id": 112,
            "staff_id": 5,
            "counterparty_id": 6,
            "units_sold": 26768,
            "unit_price": 2.64,
            "currency_id": 3,
            "agreed_delivery_date": "2023-11-02",
            "agreed_payment_date": "2023-11-03",
            "agreed_delivery_location_id": 10,
        },
        {
            "sales_order_id": 4982,
            "created_at": "2023-10-30T09:51:09.719",
            "last_updated": "2023-10-30T09:51:09.719",
            "design_id": 131,
            "staff_id": 15,
            "counterparty_id": 5,
            "units_sold": 66274,
            "unit_price": 3.87,
            "currency_id": 3,
            "agreed_delivery_date": "2023-11-02",
            "agreed_payment_date": "2023-11-02",
            "agreed_delivery_location_id": 6,
        },
        {
            "sales_order_id": 5035,
            "created_at": "2023-11-01T16:06:09.791",
            "last_updated": "2023-11-01T16:06:09.791",
            "design_id": 147,
            "staff_id": 1,
            "counterparty_id": 17,
            "units_sold": 65588,
            "unit_price": 2.59,
            "currency_id": 3,
            "agreed_delivery_date": "2023-11-01",
            "agreed_payment_date": "2023-11-05",
            "agreed_delivery_location_id": 17,
        }
    ]
}


# def test_output_rows_has_correct_key_names():
#     result = format_dim_date(test_table)
#     for date in result:
#         assert 'date_id' in date
#         assert 'day' in date
#         assert 'day_name' in date
#         assert 'day_of_week' in date
#         assert 'month' in date
#         assert 'month_name' in date
#         assert 'quarter' in date
#         assert 'year' in date
#     from pprint import pprint
#     pprint(result)

def test_correct_output():
    result = format_dim_date(test_table)
    assert len(result) == 5
    assert ['2023-11-01', 2023, 11, 1, 2, 'Wednesday', 'November', 3] in result
    assert ['2023-11-02', 2023, 11, 2, 3, 'Thursday', 'November', 3] in result
    assert ['2023-11-05', 2023, 11, 5, 6, 'Sunday', 'November', 3] in result
    assert ['2023-11-03', 2023, 11, 3, 4, 'Friday', 'November', 3] in result
    assert ['2023-10-30', 2023, 10, 30, 0, 'Monday', 'October', 3] in result


def test_KeyError_happend_when_wrong_table_name(caplog):
    wrong_table = {'staff': test_table['sales_order']}
    with caplog.at_level(logging.ERROR):
        format_dim_date(wrong_table)
        assert 'Error retrieving data' in caplog.text


def test_RuntimeError_happend_when_wrong_input():
    with pytest.raises(RuntimeError):
        format_dim_date(5)
