#!/usr/bin/python3
"""
0-log_queries.py
Decorator to log SQL queries executed by a function
"""

import sqlite3
import functools


def log_queries(func):
    """
    Decorator to log SQL queries executed by the function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # assume first positional arg is the SQL query
        if args:
            print(f"Executing SQL query: {args[0]}")
        elif 'query' in kwargs:
            print(f"Executing SQL query: {kwargs['query']}")
        else:
            print("No SQL query found to log")
        return func(*args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    """
    Fetch users from the users.db SQLite database
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    # Example usage
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
