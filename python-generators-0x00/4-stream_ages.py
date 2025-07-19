#!/usr/bin/python3
"""
4-stream_ages.py
Compute average user age efficiently using a generator.
"""

import seed  # assumes connect_to_prodev() is defined there


def stream_user_ages():
    """
    Generator that yields user ages one by one.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    for (age,) in cursor:
        yield age
    cursor.close()
    connection.close()


def compute_average_age():
    """
    Computes and prints the average age of users.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    average_age = total_age / count if count else 0
    print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    compute_average_age()
