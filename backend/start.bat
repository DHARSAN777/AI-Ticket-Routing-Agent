@echo off
echo Starting AI Ticket Support System Backend...
echo.
echo Make sure you have:
echo  1. Created .env file with your GEMINI_API_KEY
echo  2. MongoDB running (or will use default connection)
echo.
python -m uvicorn main:app --reload --port 8080 --host 0.0.0.0
