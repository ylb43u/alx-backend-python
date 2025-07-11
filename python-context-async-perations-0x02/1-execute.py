import sqlite3

class ExecuteQuery:    
    def __init__(self, query="SELECT * FROM users WHERE age > ?", params=(25,), db_path='users.db'):
        self.db_path = db_path
        self.query = query
        self.params = params
        self.conn = None
    
    def __enter__(self):
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.query,self.params)
            result = self.cursor.fetchall()
            return result
      
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
        # Returning False propagates exception if any
        return False    
