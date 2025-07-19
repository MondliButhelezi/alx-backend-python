#!/usr/bin/python3
"""
2-lazy_paginate.py
Lazily load user_data from the DB in pages using a generator.
"""

import seed  # assuming seed.py contains connect_to_prodev()


def paginate_users(page_size, offset):
    """Fetch a single page of users starting at offset."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches pages of users from DB.
    Yields one page (list of rows) at a time.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
