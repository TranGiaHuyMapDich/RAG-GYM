"""
Startup script for Gym RAG AI Assistant
Script khởi chạy cho ứng dụng
"""

import sys
import subprocess
import os

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 8):
        print("❌ Lỗi: Yêu cầu Python 3.8 trở lên")
        print(f"   Phiên bản hiện tại: Python {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def check_dataset():
    """Kiểm tra file dataset có tồn tại không"""
    if not os.path.exists("megaGymDataset.csv"):
        print("❌ Lỗi: Không tìm thấy file 'megaGymDataset.csv'")
        print("   Vui lòng đảm bảo file dataset nằm trong cùng thư mục với script này")
        sys.exit(1)
    else:
        print("✅ Dataset found: megaGymDataset.csv")

def install_dependencies():
    """Cài đặt dependencies"""
    print("\n📦 Đang kiểm tra và cài đặt dependencies...")
    print("   (Lần đầu chạy có thể mất 5-10 phút để tải models)\n")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
        print("✅ Đã cài đặt tất cả dependencies")
    except subprocess.CalledProcessError:
        print("⚠️ Có lỗi khi cài đặt dependencies")
        print("   Hãy thử chạy: pip install -r requirements.txt")
        response = input("\n   Bạn có muốn tiếp tục chạy ứng dụng không? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)

def create_directories():
    """Tạo các thư mục cần thiết"""
    directories = ["static", "chroma_db"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Đã tạo thư mục: {directory}")

def main():
    """Main function"""
    print("\n" + "="*70)
    print("🏋️  GYM RAG AI ASSISTANT - TRỢ LÝ GYM THÔNG MINH")
    print("="*70 + "\n")
    
    print("📋 Bước 1: Kiểm tra hệ thống...")
    check_python_version()
    check_dataset()
    
    print("\n📋 Bước 2: Tạo thư mục...")
    create_directories()
    
    print("\n📋 Bước 3: Cài đặt dependencies...")
    try:
        import fastapi
        import uvicorn
        import chromadb
        import pandas
        import sentence_transformers
        print("✅ Tất cả dependencies đã được cài đặt")
    except ImportError:
        install_dependencies()
    
    print("\n" + "="*70)
    print("🚀 KHỞI ĐỘNG ỨNG DỤNG")
    print("="*70)
    print("\n💡 Lưu ý:")
    print("   - Lần đầu chạy sẽ mất thời gian để tải models (~500MB)")
    print("   - Vector database sẽ được tạo tự động lần đầu")
    print("   - Truy cập ứng dụng tại: http://localhost:8000")
    print("   - Xem API docs tại: http://localhost:8000/docs")
    print("   - Nhấn Ctrl+C để dừng server\n")
    print("="*70 + "\n")
    
    # Chạy ứng dụng
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("👋 Đã dừng ứng dụng. Hẹn gặp lại!")
        print("="*70 + "\n")

if __name__ == "__main__":
    main()

