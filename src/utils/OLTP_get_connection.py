import os
from pg8000.native import Connection, InterfaceError, DatabaseError, Error
from dotenv import load_dotenv
load_dotenv()


def get_connection():
    '''
    This utility function allows for connections to the OLTP database - Totesys.
    '''
    try:
        print('Connection to database Totesys has been established.')
        return Connection (user=os.environ['PGUSER'],
                        host=os.environ['PGHOST'],
                        port=os.environ['PGPORT'],
                        database=os.environ['DB'],
                        password=os.environ['PGPASSWORD'],
                        )
    except (InterfaceError, DatabaseError) as error:
        print(f"pg8000 - {error} has occured.")
        return error
    except Exception as e:
        print('An error has occured when attempting to connect to the database.')
        raise e