# Followed code example from here:
# https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application

import psycopg2

username = "flaskuser"


def get_connection(password, host, database, port=5432):
    return psycopg2.connect(
        host=host,
        database=database,
        user=username,
        password=password,
        port=port)
