@echo off
chcp 65001 > nul
echo.
echo ====================================================================
echo 🏋️  GYM RAG AI ASSISTANT - TRỢ LÝ GYM THÔNG MINH
echo ====================================================================
echo.
echo 🚀 Đang khởi động ứng dụng...
echo.

python start.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Có lỗi xảy ra khi chạy ứng dụng
    echo.
    pause
)

