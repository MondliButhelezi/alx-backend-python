#!/usr/bin/python3
"""
4-cache_query.py
Decorators to handle DB connection and cache queries
"""

import sqlite3
import functools

# global cache dictionary
query_cache = {}


def with_db_connection(func):
    """
    Decorator to handle opening and closing DB connection
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def cache_query(func):
    """
    Decorator to cache query results based on SQL query string
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]
        print(f"[CACHE MISS] Executing and caching result for query: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users and cache result
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call will execute and cache
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call will use cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
