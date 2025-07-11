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

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn,*args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("[LOG] Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print("[LOG] Transaction rolled back due to error:", e)
            raise  # re-raise the exception
    return wrapper


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')