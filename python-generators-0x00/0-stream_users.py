import pymysql

def stream_users():
    """
    Generator that connects to the ALX_prodev MySQL database
    and yields rows from the user_data table one by one.
    """
    connection_params = {
        "host": "localhost",
        "user": "root",    
        "password": "", 
        "database": "ALX_prodev",
        "cursorclass": pymysql.cursors.SSCursor  # Enables streaming
    }

    connection = pymysql.connect(**connection_params)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_data")
            for row in cursor:
                yield row  # 🔁 Yield each row one at a time
    finally:
        connection.close()