import mysql.connector
from mysql.connector import pooling

db_config = {
    'host': 'localhost',
    'user': 'root',       # !!! Впиши свій логін
    'password': '6541230987Mm', # !!! Впиши свій пароль
    'database': 'Lab_3'
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_config
)

def get_connection():
    return connection_pool.get_connection()