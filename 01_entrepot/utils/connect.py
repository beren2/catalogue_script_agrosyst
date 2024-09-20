"""
    Fonctions permettant de se connecter à une base de données
"""
import psycopg2
from utils.config import config

def connect(file_name='database_source.ini'):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config(file_name=file_name)

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

if __name__ == '__main__':
    connect()
