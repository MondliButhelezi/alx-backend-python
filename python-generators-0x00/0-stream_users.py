#!/usr/bin/python3
"""
0-stream_users.py
Generator function that streams rows from user_data table one by one.
"""

import mysql.connector


def stream_users():
    """Generator that yields rows from user_data as dictionaries"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_mysql_password",  # replace with your mysql root password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
