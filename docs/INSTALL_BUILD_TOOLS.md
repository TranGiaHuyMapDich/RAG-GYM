# Hướng Dẫn Cài Visual Studio Build Tools

## 🔧 Tại Sao Cần?

Một số Python packages (như `chroma-hnswlib`) cần C++ compiler để build.

## 📥 Cách Cài Đặt

### Bước 1: Tải Visual Studio Build Tools

**Link tải:** https://visualstudio.microsoft.com/visual-cpp-build-tools/

Hoặc trực tiếp: https://aka.ms/vs/17/release/vs_BuildTools.exe

### Bước 2: Chạy File Cài Đặt

1. Mở file `vs_BuildTools.exe` vừa tải
2. Chọn **"Desktop development with C++"**
3. Ở bên phải, đảm bảo chọn:
   - ✅ MSVC v143 - VS 2022 C++ x64/x86 build tools
   - ✅ Windows 10/11 SDK
4. Nhấn **Install** (Kích thước: ~7GB)
5. Đợi cài đặt xong (~15-30 phút)

### Bước 3: Restart Computer

Sau khi cài xong, **restart máy tính**

### Bước 4: Thử Lại

```bash
python -m pip install -r requirements.txt
```

## ⚠️ Lưu Ý

- Cần ~7GB dung lượng
- Mất ~15-30 phút cài đặt
- Phải restart máy tính sau khi cài

