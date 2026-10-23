import sqlite3
from database import DATABASE_PATH

def get_dataset_schema():
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'dataset'
        """)

        if cursor.fetchone() is None:
            return {
                "error": "No dataset uploaded yet."
            }

        cursor.execute("PRAGMA table_info(dataset)")
        columns = cursor.fetchall()

        schema = []

        for column in columns:
            schema.append({
                "column_name": column[1],
                "data_type": column[2]
            })

        return {
            "table_name": "dataset",
            "columns": schema
        }

    finally:
        connection.close()
