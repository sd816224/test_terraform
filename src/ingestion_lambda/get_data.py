import datetime as dt
import json
import logging
import pandas as pd


logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


def get_data(conn, last_fetch_ending_time=dt.datetime(2020, 1, 1)):
    '''
    Gets data from the connected database from last_fetch_ending_time


    Parameters
    ----------
    conn: database connection instance
        type: pg8000 connect object
    last_fetch_ending_time: the timestamp of the last fetched data file
        type: datetime object

    Returns
    -------
    JSON formatted updated content
    '''
    # have checked that all created_at=last_updated in sales_order,
    # need to check other tables that we can cross check if or statement work

    # query to get all table names from database
    try:
        updated_content = {}
        table_names = conn.run("""
                            SELECT table_name
                            FROM information_schema.tables
                            WHERE table_schema = 'public';
                            """)
        table_names.remove(['_prisma_migrations'])

        for table in table_names:

            # get updated content from table
            content = conn.run(f"""
                                SELECT * FROM {table[0]} WHERE created_at>:date
                                or last_updated>:date;
                                """, date={last_fetch_ending_time})

            # get all column names from the table
            columns = conn.run(f"""
                                SELECT column_name
                                FROM information_schema.columns
                                WHERE table_schema='public'
                                AND table_name= '{table[0]}'
                                """)
            column_names = [name[0] for name in columns]

            # integrate column names and conn to the dataframe
            df = pd.DataFrame(content, columns=column_names)
            json_formatted = df.to_json(orient="records", date_format='iso')
            back_to_list = json.loads(json_formatted)
            updated_content[table[0]] = back_to_list

        updated_json = json.dumps(
            updated_content, indent=4, sort_keys=True, default=str)
        logger.info('Updated JSON content has been retrieved.')
        return updated_json
    except Exception as exc:
        logger.error(exc)
        raise exc
