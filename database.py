""" import mysql.connector
from mysql.connector import errorcode

def create_connection():

    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',  
        'database': 'bhargavi_text_summary',
        'raise_on_warnings': True
    }
    try:
        conn = mysql.connector.connect(**config)
        print("Connection successful.")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(f"Error: {err}")
        return None
 """


import pymysql

def create_connection():
    config = {
        'user': 'admin',
        'password': 'scalable-rds-db-x23344440',
        'host': 'scalable-rds-db-x23344440.cizdihoh0eru.us-east-1.rds.amazonaws.com',  
        'database': 'scalable-rds-db-x23344440'
    }
    try:
        conn = pymysql.connect(**config)
        print("Connection successful.")
        return conn
    except pymysql.MySQLError as err:
        print(f"Error: {err}")
        return None