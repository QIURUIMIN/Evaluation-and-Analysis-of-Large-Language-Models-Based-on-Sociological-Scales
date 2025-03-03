import sqlite3

def get_db_conn():
    conn = sqlite3.connect('database.db')
    return conn
