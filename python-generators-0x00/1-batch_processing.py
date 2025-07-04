import pymysql

connection_params = {
        "host": "localhost",
        "user": "root",    
        "password": "", 
        "database": "ALX_prodev",
        "cursorclass": pymysql.cursors.SSCursor  # Enables streaming
    }

connection = pymysql.connect(**connection_params)
        
def stream_users_in_batches(batch_size):
    try:
        with connection.cursor() as cursor:
            offset = 0
            while True:
                cursor.execute(
                    "SELECT * FROM user_data LIMIT %s OFFSET %s",
                    (batch_size, offset)
                )
                batch = cursor.fetchall()
                if not batch:
                    break
                yield batch
                offset += batch_size
    finally:
        connection.close()

def batch_processing(batch_size):
    try:
         filtered_users = []
         for batch in stream_users_in_batches(batch_size):
            # Filter users where age > 25
            over_25 = [user for user in batch if int(user['age']) > 25]
            filtered_users.extend(over_25)
         return filtered_users
    finally:
        connection.close()