import datetime as dt
import json
import logging
import pandas as pd
from pg8000 import Connection
import os
from dotenv import load_dotenv

load_dotenv()
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
        #main
        table_names = conn.run("""
                            SELECT table_name
                            FROM information_schema.tables
                            WHERE table_schema = 'public';
                            """)
        
        #original
        # table_names = conn.run("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        
        print(table_names,type(table_names))

    except Exception as exc:
        logger.error(exc)
        raise exc
    
connection_params = {
            "host": 'nc-data-eng-totesys-production.chpsczt8h1nu.eu-west-2.rds.amazonaws.com',
            "port": 5432,
            "user": 'project_user_5',
            "password": 'ykrhkJP5XlZVPevI',
            "database":'totesys',
        }

conn=Connection(
    user=connection_params['user'],
    host=connection_params['host'],
    port=connection_params['port'],
    database=connection_params['database'],
    password=connection_params['password'], timeout=5
)
# conn=Connection(
#     user=os.environ['PGUSER'],
#     host=os.environ['PGHOST'],
#     port=os.environ['PGPORT'],
#     database=os.environ['DB'],
#     password=os.environ['PGPASSWORD'], timeout=5
# )

get_data(conn)