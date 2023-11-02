import logging
from pg8000 import Connection, DatabaseError, InterfaceError


logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


def get_connection(database_credentials):
    '''
    Gets connections to the OLTP database - Totesys.


    Parameters
    ----------
    database_credentials (from the get_credentials util) - which is a dictionary consisting of:
        user
        host
        database
        port
        password

    Raises
    ------
    DatabaseError: Will return an error message showing what is missing.
        i.e. if the password is wrong, the error message will state password 
        authentication has failed.
    InterfaceError: 

    Returns
    -------
    A successful pg8000 connection object will be returned.
    '''
    try:
        user=database_credentials['user']
        host=database_credentials['host']
        database=database_credentials['database']
        port=database_credentials['port']
        password=database_credentials['password']
        conn= Connection(user, host, database, port, password, timeout=1)
        logger.info('Connection to database Totesys has been established.')
        return conn
    except DatabaseError as db:
        logger.error(f"pg8000 - an error has occured: {db.args[0]['M']}")
        raise db
    except InterfaceError as ie:
        logger.error(f'pg8000 - an error has occured: \n"{ie}"')
        raise ie
    except Exception as exc:
        logger.error('An error has occured when attempting to connect to the database.')
        raise exc

