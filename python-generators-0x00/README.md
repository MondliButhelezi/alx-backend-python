# Python Generators Project: Database Seeder

## Overview

This script sets up the MySQL database `ALX_prodev`, creates a table `user_data`, and populates it with data from a CSV file.

### Table Schema

| Column   | Type      | Description                 |
|----------|-----------|-----------------------------|
| user_id  | UUID      | Primary Key, Indexed       |
| name     | VARCHAR   | Not Null                   |
| email    | VARCHAR   | Not Null                   |
| age      | DECIMAL   | Not Null                   |

### Files

- `seed.py` — Script to create database, table, and insert data.
- `user_data.csv` — CSV file containing sample user data.

### Usage

Run the script via `0-main.py` as provided:

```bash
./0-main.py
