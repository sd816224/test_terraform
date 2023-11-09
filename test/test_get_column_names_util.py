from src.loading_lambda.get_column_names_util import (
    get_column_names,
    get_connection,
    get_credentials,
)
import logging

logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)


def test_real_dim_counterparty_columns():
    secret_name = "totesys-warehouse"
    credentials = get_credentials(secret_name)
    conn = get_connection(credentials)
    result = get_column_names(conn, "dim_counterparty")
    assert (
        result
        == "('counterparty_id', 'counterparty_legal_name', 'counterparty_legal_address_line_1', 'counterparty_legal_address_line_2', 'counterparty_legal_district', 'counterparty_legal_city', 'counterparty_legal_postal_code', 'counterparty_legal_country', 'counterparty_legal_phone_number')"
    )  # noqa E501


def test_real_dim_currency_columns():
    secret_name = "totesys-warehouse"
    credentials = get_credentials(secret_name)
    conn = get_connection(credentials)
    result = get_column_names(conn, "dim_currency")
    assert result == "('currency_id', 'currency_code', 'currency_name')"


# def test_real_dim_date_columns():
#     secret_name = "totesys-warehouse"
#     credentials = get_credentials(secret_name)
#     conn = get_connection(credentials)
#     result = get_column_names(conn, 'dim_date')
#     assert result == "('quarter', 'year', 'month', 'day', 'day_of_week', 'date_id', 'month_name', 'day_name')"  # noqa E501


def test_real_dim_design_columns():
    secret_name = "totesys-warehouse"
    credentials = get_credentials(secret_name)
    conn = get_connection(credentials)
    result = get_column_names(conn, "dim_design")
    assert (
        result == "('design_id', 'design_name', 'file_location', 'file_name')"
    )  # noqa E501


def test_real_dim_location_columns():
    secret_name = "totesys-warehouse"
    credentials = get_credentials(secret_name)
    conn = get_connection(credentials)
    result = get_column_names(conn, "dim_location")
    assert (
        result
        == "('location_id', 'address_line_1', 'address_line_2', 'district', 'city', 'postal_code', 'country', 'phone')"
    )  # noqa E501


def test_real_dim_staff_columns():
    secret_name = "totesys-warehouse"
    credentials = get_credentials(secret_name)
    conn = get_connection(credentials)
    result = get_column_names(conn, "dim_staff")
    assert (
        result
        == "('staff_id', 'first_name', 'last_name', 'department_name', 'location', 'email_address')"
    )  # noqa E501


def test_real_dim_currency_columns_incorrect_table_name(caplog):
    with caplog.at_level(logging.INFO):
        secret_name = "totesys-warehouse"
        credentials = get_credentials(secret_name)
        conn = get_connection(credentials)
        get_column_names(conn, "wrong_table_name")
        assert "Incorrect table name has been provided." in caplog.text
