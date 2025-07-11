import time
import sqlite3 
import functools

#### paste your with_db_decorator here

""" your code goes here"""

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def retry_on_failure(retries=3, delay=1):
   def decorator(func):
        @functools.wraps(func)
        def wrapper(conn,*args, **kwargs):
            last_exception = None
            for attempt in range(0,retries):            
                try:
                    conn.commit()
                    return func(conn,*args, **kwargs)
                except Exception as e:
                    print(f"[Retry] Attempt {attempt} failed with error: {e}")
                    last_exception = e
                    time.sleep(delay)
            # If all retries failed, raise last exception
            raise last_exception
        return wrapper
   return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)