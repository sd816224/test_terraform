import logging
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


def format_dim_counterparty(table):
    '''
    argument:sales_order_table
        type:dict
            key: table name
            value: updated content (list of dictionary)

    return:
        type: list of lists
            for each row:
                counterparty_id: int
                counterparty_legal_name: str
                counterparty_legal_address_line_1: str
                counterparty_legal_address_line_2: str
                counterparty_legal_district: str
                counterparty_legal_city: str
                counterparty_legal_postal_code: str
                counterparty_legal_country: str
                counterparty_legal_phone_number: str
    raise:
        RuntimeError
        KeyError
    '''

    try:
        # read counterparty table content from the ingestion lambda output
        updpated_cp = table['counterparty']
        address_lookup = table['address']
        result = []
        for c in updpated_cp:
            # searching address from address_look_up_table
            address = [r for r in address_lookup if r['address_id'] == c['legal_address_id']][0] # noqa E501
            # formating the dim table
            result.append({
                'counterparty_id': c['legal_address_id'],
                'counterparty_legal_name': c['counterparty_legal_name'],
                'counterparty_legal_address_line_1': address['address_line_1'],
                'counterparty_legal_address_line_2': address['address_line_2'],
                'counterparty_legal_district': address['district'],
                'counterparty_legal_city': address['city'],
                'counterparty_legal_postal_code': address['postal_code'],
                'counterparty_legal_country': address['country'],
                'counterparty_legal_phone_number': address['phone']
            })
        return result

    except KeyError as k:
        logger.error(f'Error retrieving data, {k}')

    except Exception as e:
        logger.error(e)
        raise RuntimeError
