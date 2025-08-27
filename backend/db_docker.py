import mysql.connector
from mysql.connector import pooling

dbconfig = {
    "host": "db",               # Docker service name from docker-compose.yml
    "user": "research_user",
    "password": "research_pass",
    "database": "research_db"
}

cnxpool = pooling.MySQLConnectionPool(pool_name="ra_docker_pool", pool_size=5, **dbconfig)

def get_conn():
    return cnxpool.get_connection()
