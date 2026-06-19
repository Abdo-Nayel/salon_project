"""Create local PostgreSQL database from .env if missing."""
import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / '.env')

DB_NAME = os.environ.get('DB_NAME', 'Nayel')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = os.environ.get('DB_PORT', '5432')


def main():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
    except psycopg2.Error as exc:
        print(f'Cannot connect to PostgreSQL: {exc}')
        print('Check DB_USER / DB_PASSWORD / DB_HOST in .env')
        sys.exit(1)

    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('SELECT 1 FROM pg_database WHERE datname = %s', (DB_NAME,))
    if cur.fetchone():
        print(f'Database already exists: {DB_NAME}')
    else:
        cur.execute(f'CREATE DATABASE "{DB_NAME}"')
        print(f'Created database: {DB_NAME}')

    cur.close()
    conn.close()
    print('Done. Now run: python manage.py migrate')


if __name__ == '__main__':
    main()
