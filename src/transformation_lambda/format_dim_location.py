import logging

logging.basicConfig()
logger = logging.getLogger("transformation_lambda")
logger.setLevel(logging.INFO)


def format_dim_location(address_json):
    """
    Formats the address data ready to be inserted
    into the dim_location table.

    Parameters
    ----------
        address_json: JSON, required.
            The JSON file to be transformed into parquet.

    Raises
    ------

    KeyError:
        If the address key is missing.
        If any of the columns are missing.

    Returns
    -------
        A list of lists.
    """
    dim_location = []
    try:
        addresses = address_json["address"]
        for address in addresses:
            insert = True
            row = [
                address["address_id"],
                address["address_line_1"],
                address["address_line_2"],
                address["district"],
                address["city"],
                address["postal_code"],
                address["country"],
                address["phone"],
            ]
            for list in dim_location:
                if list == row:
                    insert = False
            if insert is True:
                dim_location.append(row)
        return dim_location
    except KeyError as ke:
        logger.error(f"KeyError: missing key {ke}.")
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
