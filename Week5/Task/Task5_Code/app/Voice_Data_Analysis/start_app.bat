@echo off
cd /d "%~dp0"

echo Starting Voice Data Analyst...

set "PYTHON=C:\Users\moham\Downloads\NLP_Cellula\NLP_Cellula_Internship\Week5\Task\Task5_Code\.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo Virtual environment not found at:
    echo %PYTHON%
    pause
    exit /b 1
)

start "" http://127.0.0.1:8000/ui/

"%PYTHON%" -m uvicorn main:app --reload

pause