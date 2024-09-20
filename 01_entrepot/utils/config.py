"""
    Fonctions permettant de lire les paramètres du fichier de configuration
"""

from configparser import ConfigParser


def config(file_name='database.ini', section='postgresql'):
    """
        Retourne un dictionnaire des paramètres de configuration déclarés dans le fichier.
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(file_name)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {0} not found in the {1} file'.format(section, file_name))

    return db
