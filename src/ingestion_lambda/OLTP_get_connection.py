# import os
import logging
from pg8000.native import Connection, InterfaceError, DatabaseError, Error
# from dotenv import load_dotenv


logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)

def get_connection(user, host, database, port, password):
    '''
    This utility function allows for connections to the OLTP database - Totesys.
    '''
    try:
        load_dotenv()
        logger.info('Connection to database Totesys has been established.')
        return Connection(user, host, database, port, password)

    except (InterfaceError, DatabaseError) as e:
        logger.error('pg8000 - an error has occured.')
        raise e
    except Exception as exc:
        logger.error('An error has occured when attempting to connect to the database.')
        raise exc

