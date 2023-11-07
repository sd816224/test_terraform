from datetime import datetime as dt
import logging

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


def format_dim_date(sales_order_table):
    '''
    argument:sales_order_table
        type:dict
            key: table name
            value: updated content (list of dictionary)

    return:
        type: list of list
            for each row:
                date_id:datetime (date ('%Y-%m-%d'))
                year:year of the date (int)
                month:month of the date (int)
                day:day of the date (int)
                day_of_week:weekday of date,0 for monday,6 for sunday(int)
                day_name:weekday name of the date (str)
                month_name: month name of the date (str)
                quarter: quarter of the date (int)
    raise:
        RuntimeError
        KeyError

    question:
        when running every 10mins if having sale_order
        and without accessing the data warehouse
        do we assert new line again and again for the same date?
        do we need to avoid it? how?

        im guessing the logic all done by loading lambda maybe
    '''
    try:
        # read updated content from input table
        content = sales_order_table['sales_order']

        # extract all date objects from table
        all_dates = []
        for row in content:
            all_dates += [dt.strptime(row['agreed_delivery_date'], '%Y-%m-%d'),
                          dt.strptime(row['agreed_payment_date'], '%Y-%m-%d'),
                          dt.strptime(row['created_at'][:10], '%Y-%m-%d'),
                          dt.strptime(row['last_updated'][:10], '%Y-%m-%d')]

        # remove the duplicate date
        remove_duplicate = list(set(all_dates))

        # formatting
        result = []
        for date in remove_duplicate:
            result.append({
                'date_id': date.strftime('%Y-%m-%d'),
                'year': date.year,
                'month': date.month,
                'day': date.day,
                'day_of_week': date.weekday(),
                'day_name': date.strftime('%A'),
                'month_name': date.strftime('%B'),
                'quarter': 1 + (dt(2020, 9, 1).month - 1) // 3,
            })

        # transfer to list of list
        list_list = []
        for row in result:
            list_list.append([
                row['date_id'],
                row['year'],
                row['month'],
                row['day'],
                row['day_of_week'],
                row['day_name'],
                row['month_name'],
                row['quarter'],
                ])
        return list_list

    except KeyError as k:
        logger.error(f'Error retrieving data, {k}')

    except Exception as e:
        logger.error(e)
        raise RuntimeError
