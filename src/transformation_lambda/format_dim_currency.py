import logging

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)

currency_name = {
    "GBP": "Pound Sterling",
    "USD": "United States dollar",
    "EUR": "Euros",
}


def format_dim_currency(currency_table):
    '''
    Formats the ingested currency table into the correct format.

    Parameters
    ----------
    currency_table json

    Raises
    ------
    KeyError: Will return an error message, if the
        passed table has an incorrect key.
    RuntimeError: Returns an error when passed a wrong
        argument

    Returns
    -------
    A successful list of lists, containing a correctly formatted
    dim_currency table with the column names:
        currency_id
        currency_code
        currency_name
    '''
    try:
        content = currency_table['currency']

        all_currencies = []
        for row in content:

            all_currencies.append({
                'currency_id': row['currency_id'],
                'currency_code': row['currency_code'],
                'currency_name': currency_name[row['currency_code']]
            })
        print(all_currencies)
        return all_currencies

    except KeyError as k:
        logger.error(f'Error retrieving data, {k}')

    except Exception as e:
        logger.error(e)
        raise RuntimeError
