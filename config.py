import os

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
