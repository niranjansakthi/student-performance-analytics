import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_NAME = "advanced_student_management"

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="ranju123",
    dbname="postgres"
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
exists = cur.fetchone()

if not exists:
    cur.execute('CREATE DATABASE ' + DB_NAME)
    print("[OK] Database '" + DB_NAME + "' created successfully.")
else:
    print("[OK] Database '" + DB_NAME + "' already exists.")

cur.close()
conn.close()
