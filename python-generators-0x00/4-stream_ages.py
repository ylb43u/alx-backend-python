import pymysql

connection_params = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "ALX_prodev",
        "cursorclass": pymysql.cursors.SSCursor  # Streaming cursor
    }

connection = pymysql.connect(**connection_params)


def stream_user_ages():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT age FROM user_data")
            for row in cursor:
                yield float(row[0])  # Ensure age is numeric
    finally:
        connection.close()
        
def calculate_average_age():
    """
    Calculates and prints the average age of users using the generator.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    