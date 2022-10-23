# Followed code example from here:
# https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application

import os
import psycopg2


def db_init_test():
    os.environ['DB_PASSWORD'] = ""
    password = os.environ['DB_PASSWORD']

    os.environ['DB_USERNAME'] = "flaskuser"
    username = os.environ['DB_USERNAME']

    conn = psycopg2.connect(
        host="172.17.0.2",
        database="RobotRadarAlpha",
        user=username,
        password=password)

    cur = conn.cursor()

    cur.execute('INSERT INTO "Map" DEFAULT VALUES returning "Id";')

    # cur.execute('INSERT INTO books (title, author, pages_num, review)'
    #            'VALUES (%s, %s, %s, %s)',
    #            ('A Tale of Two Cities',
    #             'Charles Dickens',
    #             489,
    #             'A great classic!')
    #            )

    conn.commit()

    cur.close()
    conn.close()

    print("Successfully inserted some junk!")
