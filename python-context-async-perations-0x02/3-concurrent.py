#!/usr/bin/env python3
"""
Running Concurrent Asynchronous Database Queries with aiosqlite.

This script illustrates how to execute multiple database queries at the same time
using Python’s asyncio library in combination with aiosqlite. Instead of running
queries one after another, this approach allows independent queries to run in
parallel, improving efficiency and reducing wait times.
"""

import asyncio
import aiosqlite
import sqlite3
import os
import time
from typing import List, Tuple


async def async_fetch_users() -> List[Tuple]:
    """
    Retrieve all users asynchronously from the database.
    
    Opens a non-blocking connection to an SQLite database, executes a query
    to pull all user records, and then returns the results.
    
    Returns:
        List[Tuple]: A list of tuples with user information (id, name, email, age)
    """
    db_name = "sample_database.db"
    
    try:
        print("🔍 Running async_fetch_users...")
        start_time = time.time()
        
        async with aiosqlite.connect(db_name) as db:
            async with db.execute("SELECT * FROM users ORDER BY name") as cursor:
                users = await cursor.fetchall()
                
        elapsed = time.time() - start_time
        
        print(f"✅ async_fetch_users finished in {elapsed:.4f} seconds")
        print(f"   Retrieved {len(users)} users")
        
        return users
        
    except Exception as e:
        print(f"❌ Problem in async_fetch_users: {e}")
        return []


async def async_fetch_older_users() -> List[Tuple]:
    """
    Retrieve users older than 40 asynchronously.
    
    Connects to the database in async mode, runs a parameterized query
    filtering users above the age of 40, and returns the results.
    
    Returns:
        List[Tuple]: A list of tuples containing user data for users older than 40
    """
    db_name = "sample_database.db"
    age_limit = 40
    
    try:
        print("🔍 Running async_fetch_older_users...")
        start_time = time.time()
        
        async with aiosqlite.connect(db_name) as db:
            async with db.execute(
                "SELECT * FROM users WHERE age > ? ORDER BY age DESC",
                (age_limit,)
            ) as cursor:
                older_users = await cursor.fetchall()
                
        elapsed = time.time() - start_time
        
        print(f"✅ async_fetch_older_users finished in {elapsed:.4f} seconds")
        print(f"   Retrieved {len(older_users)} users older than {age_limit}")
        
        return older_users
        
    except Exception as e:
        print(f"❌ Problem in async_fetch_older_users: {e}")
        return []


async def fetch_concurrently():
    """
    Run multiple queries at the same time using asyncio.gather().
    
    This shows how to start more than one async database query at once.
    By executing them concurrently with asyncio.gather(), overall runtime
    is reduced compared to running them sequentially.
    
    Returns:
        Tuple[List[Tuple], List[Tuple]]: Results from both queries
    """
    print("\n" + "="*70)
    print("🚀 STARTING PARALLEL DATABASE QUERIES")
    print("="*70)
    
    overall_start = time.time()
    
    try:
        print("\n📊 Running queries in parallel...")
        print("-" * 50)
        
        all_users, older_users = await asyncio.gather(
            async_fetch_users(),
            async_fetch_older_users()
        )
        
        elapsed = time.time() - overall_start
        
        print("\n🎉 Both queries finished!")
        print(f"⏱️  Total time: {elapsed:.4f} seconds")
        
        return all_users, older_users
        
    except Exception as e:
        print(f"❌ Error while running concurrent queries: {e}")
        return [], []


async def demonstrate_sequential_vs_concurrent():
    """
    Compare sequential vs concurrent performance.
    
    Runs the same database queries both one after the other and in parallel,
    so the speed difference between the two approaches can be observed.
    """
    print("\n" + "="*70)
    print("⚡ PERFORMANCE TEST: SEQUENTIAL vs CONCURRENT")
    print("="*70)
    
    # Sequential run
    print("\n1️⃣ SEQUENTIAL EXECUTION")
    print("-" * 30)
    
    start_seq = time.time()
    users_seq = await async_fetch_users()
    older_seq = await async_fetch_older_users()
    seq_time = time.time() - start_seq
    
    print(f"⏱️  Time taken sequentially: {seq_time:.4f} seconds")
    
    # Concurrent run
    print("\n2️⃣ CONCURRENT EXECUTION")
    print("-" * 30)
    
    start_conc = time.time()
    users_conc, older_conc = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    conc_time = time.time() - start_conc
    
    print(f"⏱️  Time taken concurrently: {conc_time:.4f} seconds")
    
    # Performance improvement
    if conc_time > 0:
        speedup = seq_time / conc_time
        gain = ((seq_time - conc_time) / seq_time) * 100
        print("\n📈 PERFORMANCE RESULTS")
        print("-" * 25)
        print(f"🚀 Speedup: {speedup:.2f}x faster")
        print(f"⚡ Efficiency gain: {gain:.1f}%")
    
    return (users_seq, older_seq), (users_conc, older_conc)


def setup_sample_database(db_name):
    """
    Build a demo SQLite database with a users table.
    
    Args:
        db_name (str): Database filename
    """
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER
            )
        ''')
        
        demo_users = [
            ('Alice Johnson', 'alice@example.com', 28),
            ('Bob Smith', 'bob@example.com', 35),
            ('Charlie Brown', 'charlie@example.com', 22),
            ('Diana Prince', 'diana@example.com', 30),
            ('Edward Norton', 'edward@example.com', 42),
            ('Fiona Green', 'fiona@example.com', 19),
            ('George Wilson', 'george@example.com', 55),
            ('Helen Davis', 'helen@example.com', 26),
            ('Ivan Rodriguez', 'ivan@example.com', 33),
            ('Julia Kim', 'julia@example.com', 29),
            ('Kevin Brown', 'kevin@example.com', 48),
            ('Laura White', 'laura@example.com', 52),
            ('Michael Chen', 'michael@example.com', 41),
            ('Nancy Taylor', 'nancy@example.com', 38),
            ('Oliver Jones', 'oliver@example.com', 45),
            ('Patricia Wilson', 'patricia@example.com', 50),
            ('Quinn Davis', 'quinn@example.com', 27),
            ('Rachel Green', 'rachel@example.com', 43),
            ('Samuel Lee', 'samuel@example.com', 31),
            ('Tina Martinez', 'tina@example.com', 46)
        ]
        
        cur.execute('DELETE FROM users')
        cur.executemany(
            'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
            demo_users
        )
        
        conn.commit()
        conn.close()
        print(f"📊 Demo database '{db_name}' created with {len(demo_users)} entries")
        
    except sqlite3.Error as e:
        print(f"❌ Database setup failed: {e}")


def display_results(results, title="Query Results"):
    """
    Nicely print query output in a table.
    
    Args:
        results (List[Tuple]): Rows returned by the query
        title (str): Heading for the table
    """
    print(f"\n📋 {title}")
    print("=" * len(f"📋 {title}"))
    
    if results:
        print(f"{'ID':<5} {'Name':<15} {'Email':<25} {'Age':<5}")
        print("-" * 55)
        for row in results:
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3] or 'N/A':<5}")
        print(f"\nTotal records: {len(results)}")
    else:
        print("No data returned.")
    print()


async def main():
    """
    Orchestrates the async query demo.
    """
    db_name = "sample_database.db"
    
    setup_sample_database(db_name)
    
    try:
        # Demo concurrent queries
        all_users, older_users = await fetch_concurrently()
        display_results(all_users, "All Users (Concurrent)")
        display_results(older_users, "Users Over 40 (Concurrent)")
        
        # Compare sequential vs concurrent performance
        await demonstrate_sequential_vs_concurrent()
        
        # Show error-handling example
        print("\n" + "="*70)
        print("🛡️  ERROR HANDLING DEMO")
        print("="*70)
        
        try:
            results = await asyncio.gather(
                async_fetch_users(),
                async_fetch_older_users(),
                return_exceptions=True
            )
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"❌ Query {i+1} failed: {result}")
                else:
                    print(f"✅ Query {i+1} returned {len(result)} records")
                    
        except Exception as e:
            print(f"❌ Problem during error handling demo: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error in main: {e}")
    
    finally:
        if os.path.exists(db_name):
            os.remove(db_name)
            print(f"\n🧹 Removed sample database '{db_name}'")


if __name__ == "__main__":
    print("🎯 Starting Async Database Queries Example")
    print("📚 Using asyncio.gather() + aiosqlite for concurrency")
    
    asyncio.run(main())
