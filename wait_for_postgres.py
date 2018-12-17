# This script is needed for gitlab CI
# It waits until postgres is up and ready to process queries

import os
import time
import psycopg2


def is_postgress_ready(host, user, password, dbname, port=5432):
    c = None
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            dbname=dbname,
            password=password
        )
        c = conn.cursor()
        c.execute('SELECT 1')
        c.fetchone()
    except psycopg2.OperationalError as e:
        print(e)
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()
    return True


if __name__ == '__main__':
    while True:
        pg_ready = is_postgress_ready(
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT'),
            user=os.environ.get('DB_USER'),
            dbname=os.environ.get('DB_NAME'),
            password=os.environ.get('DB_PASSWORD'),
        )
        if pg_ready:
            exit(0)
        time.sleep(1)
