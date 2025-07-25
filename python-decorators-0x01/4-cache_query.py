import time
import sqlite3 
import functools



"""your code goes here"""

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn,*args, **kwargs):
       query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else '')       
       if query is None:
            # No query passed, just call the function
            return func(conn, *args, **kwargs)
                # Check cache first
       if query in query_cache:
            print("[CACHE] Returning cached result")
            return query_cache[query]
        # Call the function to get fresh result
       result = func(conn, *args, **kwargs)
       # Cache the result
       query_cache[query] = result
       return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")