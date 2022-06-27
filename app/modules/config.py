import os

def config():
    db = {
        'host': os.environ['DB_HOST'],
        'database': os.environ['POSTGRES_DB'],
        'user': os.environ['POSTGRES_USER'],
        'password': os.environ['POSTGRES_PASSWORD']
    }

    return db