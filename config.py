# config.py
import pymysql.cursors

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'tickets',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

