import os
import pandas as pd

DATABASE_FILE = "Toxic_database.csv"

def save_result(input_type, text, classification):
    
    toxic_data = pd.DataFrame([{
        "input_type": input_type,
        "input_text": text,
        "classification": classification
    }])

    if os.path.exists(DATABASE_FILE):

        toxic_data.to_csv(
            DATABASE_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        toxic_data.to_csv(
            DATABASE_FILE,
            mode="w",
            header=True,
            index=False
        )


def load_results():

    if os.path.exists(DATABASE_FILE):
        return pd.read_csv(DATABASE_FILE)

    return pd.DataFrame(
        columns=[
            "input_type",
            "input_text",
            "classification"
        ]
    )

