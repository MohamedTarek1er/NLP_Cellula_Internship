import sqlite3
from database import DATABASE_PATH

MAX_RESULT_ROWS = 1000

def validate_sql(sql_query: str):
    if not sql_query or not sql_query.strip():
        return False, "SQL query cannot be empty."

    query = sql_query.strip()

    first_word = query.split(None, 1)[0].upper()
    if first_word not in {"SELECT", "WITH"}:
        return False, "Only SELECT queries are allowed."

    return True, "SQL query passed the basic validation."


def execute_sql(sql_query: str):
    is_valid, message = validate_sql(sql_query)

    if not is_valid:
        return {"error": message}

    if not DATABASE_PATH.exists():
        return {"error": "No database found. Upload a dataset first."}

    connection = None

    try:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.execute("PRAGMA query_only = ON")

        def authorize(action, arg1, arg2, database_name, trigger_name):
            if action == sqlite3.SQLITE_SELECT:
                return sqlite3.SQLITE_OK

            if action == sqlite3.SQLITE_RECURSIVE:
                return sqlite3.SQLITE_OK

            if action == sqlite3.SQLITE_READ:
                if arg1 == "dataset":
                    return sqlite3.SQLITE_OK

                return sqlite3.SQLITE_DENY

            if action == sqlite3.SQLITE_FUNCTION:
                return sqlite3.SQLITE_OK

            return sqlite3.SQLITE_DENY

        connection.set_authorizer(authorize)
        cursor = connection.cursor()
        cursor.execute(sql_query)

        columns = [
            description[0]
            for description in (cursor.description or [])
        ]

        rows = cursor.fetchmany(MAX_RESULT_ROWS + 1)
        truncated = len(rows) > MAX_RESULT_ROWS
        rows = rows[:MAX_RESULT_ROWS]

        results = [
            dict(zip(columns, row))
            for row in rows
        ]

        return {
            "sql_query": sql_query,
            "columns": columns,
            "rows": results,
            "row_count": len(results),
            "truncated": truncated
        }

    except sqlite3.Error as error:
        return {
            "error": f"SQL execution failed: {error}"
        }

    finally:
        if connection is not None:
            connection.close()
