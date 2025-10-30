@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ====================================================================
echo          🏋️  GYM RAG AI ASSISTANT - TRỢ LÝ GYM THÔNG MINH
echo ====================================================================
echo.
echo 🚀 Đang khởi động ứng dụng...
echo.
echo 💡 Lần đầu chạy sẽ tải AI models (~500MB) và tạo embeddings (~2-5 phút)
echo    Lần sau sẽ chạy ngay lập tức!
echo.
echo 📌 Sau khi khởi động xong, hãy mở trình duyệt:
echo    👉 http://localhost:8000
echo.
echo ⏸️  Nhấn Ctrl+C để dừng server
echo.
echo ====================================================================
echo.

python app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Có lỗi xảy ra!
    echo.
    pause
)

