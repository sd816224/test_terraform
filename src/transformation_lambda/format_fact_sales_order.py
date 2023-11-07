import logging

logging.basicConfig()
logger = logging.getLogger("transformation_lambda")
logger.setLevel(logging.INFO)


def format_fact_sales_order(sales_order_json):
    """
    Formats the sales_order data ready to be inserted
    into the fact_sales_order table.

    Parameters
    ----------
        sales_order_json: JSON, required.
            The JSON file to be transformed into parquet.

    Raises
    ------

    KeyError:
        If the sales_order key is missing.
        If any of the columns are missing.

    Returns
    -------
        A list of lists.
    """
    json = sales_order_json["sales_order"]
    sales_order_parquet = []
    try:
        for sale in json:
            insert = True
            created_date = sale["created_at"][:10]
            created_time = sale["created_at"][11:19]
            last_updated_date = sale["last_updated"][:10]
            last_updated_time = sale["last_updated"][11:19]
            row = [
                sale["sales_order_id"],
                created_date,
                created_time,
                last_updated_date,
                last_updated_time,
                sale["staff_id"],
                sale["counterparty_id"],
                sale["units_sold"],
                sale["unit_price"],
                sale["currency_id"],
                sale["design_id"],
                sale["agreed_payment_date"],
                sale["agreed_delivery_date"],
                sale["agreed_delivery_location_id"],
            ]
            for list in sales_order_parquet:
                if list == row:
                    insert = False
            if insert is True:
                sales_order_parquet.append(row)
        return sales_order_parquet
    except KeyError as ke:
        logger.error(f"KeyError: missing key {ke}.")
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
