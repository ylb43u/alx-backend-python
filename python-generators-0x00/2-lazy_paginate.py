import pymysql

def paginate_users(page_size, offset):
    """
    Fetch a single page of users starting at the given offset.
    Yields one row at a time.
    """
    connection_params = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "ALX_prodev",
        "cursorclass": pymysql.cursors.SSCursor  # Streaming cursor
    }

    connection = pymysql.connect(**connection_params)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
            for row in cursor:
                yield row
    finally:
        connection.close()


def lazy_paginate(page_size):
    """
    Lazily paginates through all user_data rows in the database,
    using paginate_users() to fetch each page as needed.
    """
    offset = 0
    while True:
        rows_fetched = False
        for row in paginate_users(page_size, offset):
            yield row
            rows_fetched = True
        if not rows_fetched:
            break
        offset += page_size
