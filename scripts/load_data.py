import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_batch
import time


# ===============================
# DATABASE CONFIGURATION
# ===============================

DB_NAME = "heart_disease_db"  # Database name
DB_USER = "env.PGUSER"  # Use environment variable for security
DB_PASSWORD = "env.PGPASSWORD"  # Use environment variable for security
DB_HOST = "localhost"
DB_PORT = "5432"

TABLE_NAME = "heart_disease"

DATA_FILE = "../data/Heart_disease_cleaned.csv"


# ===============================
# MAP PANDAS DTYPES TO SQL TYPES
# ===============================

def map_dtype(dtype):
    if "int64" in str(dtype):
        return "INTEGER"
    elif "float64" in str(dtype):
        return "FLOAT"
    else:
        return "TEXT"


# ===============================
# CREATE TABLE
# ===============================

def create_table(conn, df):
    cursor = conn.cursor()

    columns = []
    for col, dtype in zip(df.columns, df.dtypes):
        sql_type = map_dtype(dtype)
        columns.append(f"{col} {sql_type}")

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {', '.join(columns)}
    );
    """

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()

    print("✅ Table created or already exists.")


# ===============================
# INSERT DATA
# ===============================

def insert_data(conn, df):
    cursor = conn.cursor()

    # Optional: Clear existing data before insert
    cursor.execute(f"TRUNCATE TABLE {TABLE_NAME};")
    conn.commit()

    columns = list(df.columns)
    values_placeholder = ", ".join(["%s"] * len(columns))

    insert_query = f"""
        INSERT INTO {TABLE_NAME} ({', '.join(columns)})
        VALUES ({values_placeholder})
    """

    data_tuples = [tuple(row) for row in df.to_numpy()]

    start_time = time.time()

    execute_batch(cursor, insert_query, data_tuples, page_size=1000)

    conn.commit()
    cursor.close()

    end_time = time.time()

    print(f"✅ Inserted {len(data_tuples)} rows successfully.")
    print(f"⏱ Time taken: {round(end_time - start_time, 2)} seconds")


# ===============================
# MAIN FUNCTION
# ===============================

def main():

    try:
        print("🔹 Reading cleaned dataset...")
        df = pd.read_csv(DATA_FILE)

        print("🔹 Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        print("Connected to database.")

        create_table(conn, df)
        insert_data(conn, df)

        conn.close()
        print("Data load completed successfully.")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()