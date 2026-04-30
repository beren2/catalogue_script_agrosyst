"""
    Fonctions permettant de se connecter à une base de données
"""
import psycopg2
from psycopg2 import OperationalError, InterfaceError, DatabaseError
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
    except OperationalError as e:
        # Erreur liée à l'opération (ex: serveur inaccessible, identifiants incorrects)
        print(f"Erreur de connexion à la base de données: {e}")
        return None
    except InterfaceError as e:
        # Erreur liée à l'interface (ex: problème avec le curseur)
        print(f"Erreur d'interface avec la base de données: {e}")
        return None
    except DatabaseError as e:
        # Erreur générale liée à la base de données (ex: requête invalide)
        print(f"Erreur de base de données: {e}")
        return None
    except Exception as error: # pylint: disable=broad-exception-caught
        # Filet de sécurité pour les erreurs non anticipées
        print(f"Erreur inattendue: {e}")
        return None

if __name__ == '__main__':
    connect()
