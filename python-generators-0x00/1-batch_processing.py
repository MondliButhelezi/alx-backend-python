#!/usr/bin/python3
"""
1-batch_processing.py
Batch process users in batches and filter age > 25.
"""

import seed  # assumes connect_to_prodev() is defined


def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users of size batch_size.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    offset = 0

    while True:
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes each batch and prints users with age > 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
