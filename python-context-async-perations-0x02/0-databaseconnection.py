import sqlite3

class DatabaseConnection :    
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.conn = None
    
    def __enter__(self):
            self.conn = sqlite3.connect(self.db_path)
            return self.conn
    
    
    def __call__(self, func):
        # Make instances usable as decorators
        def wrapper(*args, **kwargs):
            with self:
                return func(self.conn, *args, **kwargs)
      
      
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
        # Returning False propagates exception if any
        return False
    
with DatabaseConnection() as conn:    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)