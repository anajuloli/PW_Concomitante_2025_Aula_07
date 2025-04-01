from contextlib import contextmanager
import sqlite3

DB_NAME = 'dados.db'

@contextmanager
def get_db_connection(db_name=DB_NAME):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        yield conn
    finally:
        if conn:
            conn.commit()
            conn.close()