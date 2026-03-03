import os
import time
import psycopg2
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from psycopg2.extras import execute_batch

BASE_DIR   = Path(__file__).resolve().parent.parent
ENV_FILE   = BASE_DIR / ".env"
DATA_FILE  = BASE_DIR / "data" / "Heart_disease_cleaned.csv"
TABLE_NAME = "heart_disease"

load_dotenv(ENV_FILE)

DB_CONFIG = {
    "dbname":   os.getenv("PGDATABASE", "heart_disease_db"),
    "user":     os.getenv("PGUSER",     "postgres"),
    "password": os.getenv("PGPASSWORD"),
    "host":     os.getenv("PGHOST",     "localhost"),
    "port":     os.getenv("PGPORT",     "5432"),
}

def map_dtype(dtype):
    dtype_str = str(dtype)
    if "int64" in dtype_str:
        return "INTEGER"
    elif "float64" in dtype_str:
        return "FLOAT"
    else:
        return "TEXT"

def get_connection():
    if not DB_CONFIG["password"]:
        raise ValueError(
            "PGPASSWORD not set. Add it to your .env file:\n"
            "   PGPASSWORD=your_password"
        )
    conn = psycopg2.connect(**DB_CONFIG)
    print(f"Connected to PostgreSQL: {DB_CONFIG['dbname']} @ {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    return conn

def create_table(conn, df):
    cursor = conn.cursor()

    col_defs = ", ".join(
        f"{col} {map_dtype(dtype)}"
        for col, dtype in zip(df.columns, df.dtypes)
    )

    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME};")
    cursor.execute(f"CREATE TABLE {TABLE_NAME} ({col_defs});")
    conn.commit()
    cursor.close()

    print(f"Table '{TABLE_NAME}' created with {len(df.columns)} columns.")

def create_indexes(conn):
    cursor = conn.cursor()

    indexes = [
        f"CREATE INDEX IF NOT EXISTS idx_heartdisease ON {TABLE_NAME}(heartdisease);",
        f"CREATE INDEX IF NOT EXISTS idx_agecategory  ON {TABLE_NAME}(agecategory);",
        f"CREATE INDEX IF NOT EXISTS idx_sex          ON {TABLE_NAME}(sex);",
        f"CREATE INDEX IF NOT EXISTS idx_race         ON {TABLE_NAME}(race);",
        f"CREATE INDEX IF NOT EXISTS idx_diabetic     ON {TABLE_NAME}(diabetic);",
        f"CREATE INDEX IF NOT EXISTS idx_stroke       ON {TABLE_NAME}(stroke);",
    ]

    for idx_sql in indexes:
        cursor.execute(idx_sql)

    conn.commit()
    cursor.close()
    print("Indexes created on: heartdisease, agecategory, sex, race, diabetic, stroke")

def insert_data(conn, df):
    cursor = conn.cursor()

    cols              = list(df.columns)
    placeholders      = ", ".join(["%s"] * len(cols))
    col_names         = ", ".join(cols)
    insert_query      = f"INSERT INTO {TABLE_NAME} ({col_names}) VALUES ({placeholders})"
    data_tuples       = [tuple(row) for row in df.itertuples(index=False, name=None)]

    start_time = time.time()
    execute_batch(cursor, insert_query, data_tuples, page_size=1000)
    conn.commit()
    elapsed = round(time.time() - start_time, 2)

    cursor.close()
    print(f"Inserted {len(data_tuples)} rows in {elapsed}s")

def verify_load(conn, expected_rows):
    cursor = conn.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
    db_count = cursor.fetchone()[0]

    cursor.execute(f"""
        SELECT heartdisease, COUNT(*) AS count
        FROM {TABLE_NAME}
        GROUP BY heartdisease
        ORDER BY heartdisease;
    """)
    distribution = cursor.fetchall()

    cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 3;")
    preview = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]

    cursor.close()

    print("\nVerification Report")
    print(f"   Expected rows : {expected_rows}")
    print(f"   Loaded rows   : {db_count}")
    print(f"   Match         : {'OK' if db_count == expected_rows else 'MISMATCH'}")
    print(f"\n   HeartDisease distribution:")
    for row in distribution:
        print(f"     {row[0]:<5}: {row[1]} rows")
    print(f"\n   Preview (first 3 rows):")
    print(f"   {col_names}")
    for row in preview:
        print(f"   {list(row)}")

def main():
    print("=" * 55)
    print("Heart Disease Data Load Pipeline")
    print("=" * 55)

    print(f"\nReading cleaned dataset from:\n   {DATA_FILE}")
    if not DATA_FILE.exists():
        print("Cleaned data file not found. Run clean_data.py first.")
        return

    df = pd.read_csv(DATA_FILE)
    print(f"Dataset loaded. Shape: {df.shape}")

    try:
        conn = get_connection()
        create_table(conn, df)
        insert_data(conn, df)
        create_indexes(conn)
        verify_load(conn, expected_rows=len(df))

        conn.close()
        print("\nData load pipeline completed successfully.")

    except Exception as e:
        print(f"\nError during load: {e}")

    print("=" * 55)


if __name__ == "__main__":
    main()