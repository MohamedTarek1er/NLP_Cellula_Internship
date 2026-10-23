from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
from io import BytesIO
import pandas as pd
from schema import get_dataset_schema
from database import save_dataset
import os
import tempfile
from speech import transcribe_audio
from pydantic import BaseModel
from sql_generator import generate_sql
from sql_executor import execute_sql
from pydantic import BaseModel
from result_explainer import explain_results
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Voice-Based Data Analysis System",
    description="Analyze datasets using Arabic or English voice commands.",
    version="1.0.0",
)

STATIC_DIR = Path(__file__).resolve().parent / "static"

app.mount(
    "/ui",
    StaticFiles(directory=STATIC_DIR, html=True),
    name="frontend"
)

@app.get("/")
def home():
    return {
        "message": "Voice-Based Data Analysis API is running!",
        "supported_languages": ["Arabic", "English"],
        "status": "ready",
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):

    extension = Path(file.filename or "").suffix.lower()

    if extension not in [".csv", ".xlsx"]:
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV or XLSX file."
        )

    file_bytes = await file.read()

    try:
        if extension == ".csv":
            dataframe = pd.read_csv(BytesIO(file_bytes))
        else:
            dataframe = pd.read_excel(BytesIO(file_bytes))

        if dataframe.empty:
            raise HTTPException(
                status_code=400,
                detail="The uploaded dataset is empty."
            )

        if len(dataframe.columns) == 0:
            raise HTTPException(
                status_code=400,
                detail="The dataset has no columns."
            )

        result = save_dataset(dataframe)

        return {
            "message": "Dataset uploaded successfully!",
            "filename": file.filename,
            **result
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read the dataset: {error}"
        )
@app.get("/dataset-schema")
def dataset_schema():
    result = get_dataset_schema()

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


@app.post("/transcribe-audio")
async def transcribe_audio_endpoint(
    file: UploadFile = File(...)
):
    allowed_extensions = [
        ".wav", ".mp3", ".m4a",
        ".ogg", ".flac", ".webm"
    ]

    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format."
        )

    audio_bytes = await file.read()

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded audio file is empty."
        )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False
        ) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        result = transcribe_audio(temp_path)

        if not result["transcript"]:
            raise HTTPException(
                status_code=400,
                detail="No speech was recognized."
            )

        return {
            "message": "Audio transcribed successfully!",
            **result
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {error}"
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

class SQLQuestion(BaseModel):
    question: str

@app.post("/generate-sql")
def generate_sql_endpoint(request: SQLQuestion):
    result = generate_sql(request.question)

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


@app.post("/execute-sql")
def execute_sql_endpoint(request: SQLQuestion):
    result = execute_sql(request.question)

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


class ExplainResultsRequest(BaseModel):
    question: str
    query_result: dict


@app.post("/explain-results")
def explain_results_endpoint(
    request: ExplainResultsRequest
):
    result = explain_results(
        request.question,
        request.query_result
    )

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


@app.post("/analyze-voice")
async def analyze_voice(file: UploadFile = File(...)):
    allowed_extensions = {
        ".wav", ".mp3", ".m4a",
        ".ogg", ".flac", ".webm"
    }

    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format."
        )

    audio_bytes = await file.read()

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded audio file is empty."
        )

    temp_path = None

    try:
        # Step 1: Save the audio temporarily
        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False
        ) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        # Step 2: Convert speech into text
        transcription = transcribe_audio(temp_path)
        question = transcription["transcript"]

        if not question:
            raise HTTPException(
                status_code=400,
                detail="No speech was recognized."
            )

        # Step 3: Generate SQL from the transcribed question
        sql_result = generate_sql(question)

        if "error" in sql_result:
            raise HTTPException(
                status_code=400,
                detail=sql_result["error"]
            )

        sql_query = sql_result["sql_query"]

        # Step 4: Validate and execute the SQL query
        query_result = execute_sql(sql_query)

        if "error" in query_result:
            raise HTTPException(
                status_code=400,
                detail=query_result["error"]
            )

        # Step 5: Explain the actual SQL results
        explanation_result = explain_results(
            question,
            query_result
        )

        if "error" in explanation_result:
            raise HTTPException(
                status_code=500,
                detail=explanation_result["error"]
            )

        # Step 6: Return the complete analysis
        return {
            "message": "Voice analysis completed successfully!",
            "transcript": question,
            "language": transcription["language"],
            "sql_query": sql_query,
            "columns": query_result["columns"],
            "rows": query_result["rows"],
            "row_count": query_result["row_count"],
            "truncated": query_result["truncated"],
            "explanation": explanation_result["explanation"]
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Voice analysis failed: {error}"
        )

    finally:
        # Always delete the temporary audio file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
