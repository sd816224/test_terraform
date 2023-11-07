import logging
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


def format_dim_counterparty(table):
    '''
    formats the data to populate the dim_staff table

    Parameters
    ----------
        json with data from the counterparty table and address table.

    Raises
    ------
    KeyError
        if incorrect counterpary data or address data provided
    RuntimeError
        if an unhandled exception occurs in the try block.

    Returns
    ------
    list of lists
        each list contains everything from the updated counterparty dict

    '''

    try:
        # read counterparty table content from the ingestion lambda output
        updpated_cp = table['counterparty']
        address_lookup = table['address']
        cp_dict = []
        for cp in updpated_cp:
            # searching address from address_look_up_table
            address = [r for r in address_lookup if r['address_id'] == cp['legal_address_id']][0] # noqa E501
            # formating the dim table
            cp_dict.append({
                'counterparty_id': cp['counterparty_id'],
                'counterparty_legal_name': cp['counterparty_legal_name'],
                'counterparty_legal_address_line_1': address['address_line_1'],
                'counterparty_legal_address_line_2': address['address_line_2'],
                'counterparty_legal_district': address['district'],
                'counterparty_legal_city': address['city'],
                'counterparty_legal_postal_code': address['postal_code'],
                'counterparty_legal_country': address['country'],
                'counterparty_legal_phone_number': address['phone']
            })

            list_of_lists = []
            for row in cp_dict:
                list_of_lists.append([
                    row['counterparty_id'],
                    row['counterparty_legal_name'],
                    row['counterparty_legal_address_line_1'],
                    row['counterparty_legal_address_line_1'],
                    row['counterparty_legal_district'],
                    row['counterparty_legal_city'],
                    row['counterparty_legal_postal_code'],
                    row['counterparty_legal_country'],
                    row['counterparty_legal_phone_number']
                ])

        return list_of_lists

    except KeyError as k:
        logger.error(f'Error retrieving data, {k}')

    except Exception as e:
        logger.error(e)
        raise RuntimeError
