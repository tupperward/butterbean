from configparser import ConfigParser
import os

"""
def config(filename='database.ini', section='postgresql'):
    
    parser = ConfigParser()
    parser.read(filename)
  
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file.'.format(section, filename))
    
    return db
"""

def config():
    db = {
        'host': os.environ['PG_HOST'],
        'database': os.environ['DATABASE'],
        'user': os.environ['PG_USER'],
        'password': os.environ['PG_PASS']
    }

    return db

def sanitize(arg):
    formattedStr = arg.lower().strip()
    return formattedStr
