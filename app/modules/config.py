import os

def config():
    db = {
        'host': os.environ['DB_HOST'],
        'database': os.environ['DB_NAME'],
        'user': os.environ['DB_USER'],
        'password': os.environ['DB_PASS']
    }

    return db