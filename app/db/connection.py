import mysql.connector
from config import DB_CONFIG

def get_mysql_connection(config: dict):
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG.get('port', 3306),
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
    return conn