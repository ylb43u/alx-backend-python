import pymysql


def lazy_paginate(page_size):
    def  paginate_users(page_size, offset):
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
                cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s",(page_size,offset))
                for row in cursor:
                    yield row  # 🔁 Yield each row one at a time
        finally:
            connection.close()
    return paginate_users(page_size=page_size,offset=0)