# 🚀 Hướng Dẫn Chạy Ứng Dụng

## ⚡ Cách Chạy Nhanh Nhất

### Bước 1: Double-click file
```
run_simple.bat
```

### Bước 2: Đợi khởi động
- **Lần đầu:** 2-5 phút (tải AI models + tạo embeddings)
- **Lần sau:** ~10 giây (đã có cache)

### Bước 3: Mở trình duyệt
```
http://localhost:8000
```

---

## 📊 Quá Trình Khởi Động

Khi chạy lần đầu, bạn sẽ thấy:

```
Đang khởi tạo Gym RAG System...
Đang đọc dữ liệu từ CSV...
Đã tải 2918 bài tập
Đang tạo embeddings cho 2918 documents...
Batches:   5%|█         | 5/92 [00:10<02:45]
```

**Đừng tắt!** Hãy đợi đến khi thấy:

```
✅ Hoàn thành khởi tạo vector store!
Hệ thống RAG đã sẵn sàng!

INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## ✅ Kiểm Tra Ứng Dụng Đã Chạy

### Cách 1: Mở trình duyệt
```
http://localhost:8000
```

Nếu thấy giao diện web → **Thành công!** 🎉

### Cách 2: Kiểm tra trong terminal
Tìm dòng:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🎯 Sử Dụng Ứng Dụng

### Tab 1: 💬 Chat AI
1. Gõ câu hỏi: "Bài tập ngực cho người mới"
2. Nhấn Enter hoặc click "Gửi"
3. AI sẽ gợi ý bài tập phù hợp!

### Tab 2: 📋 Kế Hoạch Tập
1. Chọn:
   - Loại cơ thể: Mesomorph
   - Trình độ: Intermediate
   - Mục tiêu: Tăng cơ
   - Số ngày: 4 ngày/tuần
2. Nhấn "Tạo Kế Hoạch"
3. Xem lịch tập chi tiết!

### Tab 3: 🔍 Tìm Bài Tập
1. Chọn bộ lọc (nhóm cơ, thiết bị, trình độ)
2. Nhấn "Tìm Kiếm"
3. Duyệt danh sách bài tập!

### Tab 4: 📊 Thống Kê
- Xem tổng quan về 2900+ bài tập
- Phân bố theo nhóm cơ, thiết bị

---

## 🛑 Dừng Ứng Dụng

Trong terminal, nhấn: **Ctrl + C**

---

## ❓ Troubleshooting

### Vấn đề: Port 8000 đã được sử dụng
**Giải pháp:** 
1. Tắt ứng dụng đang chạy trên port 8000
2. Hoặc đổi port trong `app.py` (dòng cuối):
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Đổi 8000 → 8080
```

### Vấn đề: Mất quá lâu để tạo embeddings
**Bình thường!** Lần đầu mất 2-5 phút. Lần sau sẽ nhanh vì có cache.

### Vấn đề: Lỗi encoding/tiếng Việt
Đã fix! Nếu vẫn gặp, chạy `run_simple.bat` thay vì `python app.py`

### Vấn đề: Module not found
Chạy lại:
```bash
python -m pip install -r requirements_simple.txt
```

---

## 📁 Files Cache

Sau lần đầu chạy, sẽ tạo file:
- `embeddings_cache.pkl` (~500MB) - Lưu AI embeddings
- Lần sau chạy sẽ load từ cache, rất nhanh!

---

## 💡 Tips

1. **Để chạy nhanh lần sau:** Không xóa file `embeddings_cache.pkl`
2. **Nếu dataset thay đổi:** Xóa `embeddings_cache.pkl` để tạo lại
3. **Tiết kiệm RAM:** Đóng các ứng dụng khác khi chạy lần đầu

---

## 🎉 Chúc Bạn Sử Dụng Vui Vẻ!

**Mọi thắc mắc, xem:** README.md hoặc QUICKSTART.md

