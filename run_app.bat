@echo off
title FuzzyFit Launcher
echo =======================================
echo   FuzzyFit: App Launching...
echo =======================================
echo.

:: Activate virtual environment
if exist venv\Scripts\activate (
    echo Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo [WARNING] venv virtual environment not found. Using system python.
)

:: Run streamlit app
echo Launching Streamlit web application...
streamlit run app.py

:: If it stops, keep window open to show error
echo.
echo =======================================
echo   App stopped. Press any key to exit.
echo =======================================
pause > nul
