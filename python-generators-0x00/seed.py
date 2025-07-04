import pymysql
import pandas as pd

DB_HOST = "localhost"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "ALX_prodev"

def connect_db():
    """Connects to MySQL server (without selecting a database)."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        cursorclass=pymysql.cursors.DictCursor
    )

def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    connection.commit()

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def create_table(connection):
    """Creates the user_data table with specified fields."""
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,0) NOT NULL,
                INDEX (user_id)
            );
        """)
    connection.commit()

def insert_data(connection, data):
    """Inserts data into user_data table if email does not exist."""
    with connection.cursor() as cursor:
        for row in data:
            # Check if email already exists
            cursor.execute("SELECT 1 FROM user_data WHERE email = %s", (row['email'],))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (UUID(), %s, %s, %s)
                """, (row['name'], row['email'], int(row['age'])))
    connection.commit()

# === Main Program ===

if __name__ == "__main__":
    try:
        # Connect and setup database
        root_conn = connect_db()
        create_database(root_conn)
        root_conn.close()

        # Connect to the ALX_prodev database
        conn = connect_to_prodev()

        # Create table
        create_table(conn)

        # Load CSV data
        df = pd.read_csv("user_data.csv")
        data = df.to_dict(orient='records')

        # Insert CSV data
        insert_data(conn, data)

        print("✅ Data inserted successfully.")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        if 'conn' in locals():
            conn.close()
