#!/usr/bin/python3
"""
2-transactional.py
Decorators to handle DB connection and transactions
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator to handle opening and closing DB connection
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


def transactional(func):
    """
    Decorator to wrap function execution in a DB transaction
    Commits on success, rolls back on exception
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update user's email in the database
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


if __name__ == "__main__":
    # Update user email with transaction handling
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
