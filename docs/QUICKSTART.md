# 🚀 Quick Start - Hướng Dẫn Nhanh

## Chạy Ứng Dụng Trong 3 Bước

### 1️⃣ Cài đặt Python
Đảm bảo bạn đã cài **Python 3.8 trở lên**

Kiểm tra version:
```bash
python --version
```

### 2️⃣ Cài đặt Dependencies
```bash
pip install -r requirements.txt
```

**Lưu ý**: Lần đầu cài sẽ tải models (~500MB), mất 5-10 phút

### 3️⃣ Chạy Ứng Dụng

**Cách 1: Dùng script khởi chạy (Khuyến nghị)**
```bash
python start.py
```

**Cách 2: Chạy trực tiếp**
```bash
python app.py
```

### 4️⃣ Truy Cập
Mở trình duyệt: **http://localhost:8000**

---

## 🎯 Sử Dụng Nhanh

### Chat với AI
1. Vào tab "💬 Chat AI"
2. Gõ: "Bài tập ngực cho người mới"
3. Nhận gợi ý ngay lập tức!

### Tạo Kế Hoạch Tập
1. Vào tab "📋 Kế Hoạch Tập"
2. Chọn:
   - Loại cơ thể: Mesomorph
   - Trình độ: Intermediate
   - Mục tiêu: Tăng cơ
   - Số ngày: 4 ngày/tuần
3. Nhấn "🚀 Tạo Kế Hoạch"
4. Xem lịch tập chi tiết!

### Tìm Bài Tập
1. Vào tab "🔍 Tìm Bài Tập"
2. Chọn bộ lọc (VD: Chest + Barbell + Intermediate)
3. Nhấn "🔍 Tìm Kiếm"
4. Duyệt danh sách bài tập!

---

## ❓ Câu Hỏi Thường Gặp

**Q: Lần đầu chạy mất bao lâu?**
A: 5-10 phút để tải models và tạo vector database. Lần sau chạy rất nhanh!

**Q: Cần internet không?**
A: Chỉ cần internet lần đầu để tải models. Sau đó có thể dùng offline.

**Q: Bộ nhớ cần bao nhiêu?**
A: Tối thiểu 4GB RAM. Models chiếm ~500MB, ChromaDB ~200MB.

**Q: File dataset ở đâu?**
A: File `megaGymDataset.csv` phải nằm cùng thư mục với `app.py`

**Q: Làm sao để dừng server?**
A: Nhấn `Ctrl+C` trong terminal

---

## 🐛 Gặp Lỗi?

### Lỗi: "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### Lỗi: "Dataset not found"
Đảm bảo file `megaGymDataset.csv` trong thư mục gốc

### Lỗi: Port 8000 đang được dùng
Sửa trong `app.py`, dòng cuối:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Đổi sang port 8080
```

### Lỗi khác
Xem logs chi tiết trong terminal và kiểm tra:
- Python version >= 3.8
- Đủ dung lượng ổ cứng (~2GB)
- Đủ RAM (~4GB)

---

## 📚 Tài Liệu Đầy Đủ

Xem **README.md** để biết thêm chi tiết!

---

**💪 Chúc bạn tập luyện hiệu quả!**

