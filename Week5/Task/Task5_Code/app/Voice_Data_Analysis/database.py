import sqlite3
from pathlib import Path

DATA_FOLDER = Path(__file__).resolve().parent.parent / "Uploaded_Data"
DATA_FOLDER.mkdir(exist_ok=True)

DATABASE_PATH = DATA_FOLDER / "dataset.db"

def save_dataset(dataframe):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        dataframe.to_sql(
            "dataset",
            connection,
            if_exists="replace",
            index=False
        )
    finally:
        connection.close()

    return {
        "table_name": "dataset",
        "rows": len(dataframe),
        "columns": dataframe.columns.tolist(),
        "data_types": {
            column: str(dtype)
            for column, dtype in dataframe.dtypes.items()
        }
    }
