import os
from pg8000.native import Connection, InterfaceError, DatabaseError, Error
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


user=os.environ['PGUSER']
host=os.environ['PGHOST']
port=os.environ['PGPORT']
database=os.environ['DB']
password=os.environ['PGPASSWORD']

def get_connection():
    '''
    This utility function allows for connections to the OLTP database - Totesys.
    '''
    try:
        conn = Connection(user, host, database, port, password)
        logger.info('Connection to database Totesys has been established.')
        return conn
        
    except (InterfaceError, DatabaseError) as e:
        logger.error(f"pg8000 - {e} has occured.")
        return e
    except Exception as exc:
        logger.error('An error has occured when attempting to connect to the database.')
        raise exc
    
