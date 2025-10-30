@echo off
chcp 65001 >nul
cd /d "c:\Users\trang\OneDrive\Desktop\RAG GYM"

echo ============================================================
echo STARTING GYM RAG APP WITH ALL NEW FEATURES
echo ============================================================
echo.
echo Features:
echo  - Translation (Translate exercises to Vietnamese)
echo  - Simplified Registration (Name + Email only)
echo  - User Display in Header
echo  - Auto-redirect after registration
echo.
echo Starting server...
echo.

python app.py

echo.
echo ============================================================
echo APP STOPPED
echo ============================================================
pause

