import mysql.connector
from mysql.connector import pooling

dbconfig = {
    "host": "localhost",        # Local MySQL, not 'db'
    "user": "root",             # Use root for now
    "password": "",             # XAMPP default has empty password
    "database": "research_db"
}

cnxpool = pooling.MySQLConnectionPool(pool_name="ra_pool", pool_size=5, **dbconfig)

def get_conn():
    return cnxpool.get_connection()
