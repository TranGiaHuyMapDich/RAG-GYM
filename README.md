# Gym RAG AI Assistant - Trợ Lý Gym Thông Minh

Hệ thống RAG (Retrieval-Augmented Generation) AI thông minh dành cho gym, sử dụng hơn 2,920 bài tập từ dataset để cung cấp tư vấn tập luyện cá nhân hóa.

## Mục Lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Cấu hình](#cấu-hình)
- [Chạy ứng dụng](#chạy-ứng-dụng)
- [Sử dụng](#sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

---

##  Giới thiệu

Gym RAG AI Assistant là một ứng dụng web sử dụng công nghệ RAG (Retrieval-Augmented Generation) để cung cấp tư vấn tập luyện thông minh. Hệ thống sử dụng semantic search để tìm kiếm bài tập phù hợp từ dataset 2,920 bài tập, giúp người dùng:

- Chat với AI về gym, bài tập, kỹ thuật
- Tạo kế hoạch tập luyện cá nhân hóa
- Tìm kiếm và lọc bài tập theo tiêu chí
- Quản lý dữ liệu cá nhân (nếu sử dụng Supabase)

---

## Tính năng

### Chat AI Thông Minh
- Hỏi đáp về bài tập gym, kỹ thuật, dinh dưỡng
- Tìm kiếm bài tập theo ngữ nghĩa (semantic search)
- Hỗ trợ tiếng Việt và tiếng Anh
- Gợi ý bài tập phù hợp với từng nhóm cơ

### Kế Hoạch Tập Luyện Cá Nhân Hóa
- Phân tích theo  loại cơ thể  (Ectomorph, Mesomorph, Endomorph)
- Tùy chỉnh theo  trình độ  (Beginner, Intermediate, Advanced)
- Đặt  mục tiêu  (Tăng cơ, Giảm cân, Tăng sức mạnh, Sức bền)
- Tính toán  BMI  và đưa ra lời khuyên
- Tạo lịch tập  3-6 ngày/tuần 
- Lọc theo  thiết bị có sẵn 

### Tìm Kiếm Bài Tập
- Lọc theo nhóm cơ (Chest, Back, Shoulders, Legs, v.v.)
- Lọc theo thiết bị (Barbell, Dumbbell, Machine, v.v.)
- Lọc theo cấp độ
- Xem rating và mô tả chi tiết

### Quản Lý Người Dùng (Tùy chọn - Cần Supabase)
- Đăng ký/Đăng nhập
- Lưu trữ chat history
- Lưu trữ workout plans
- Bài tập yêu thích
- Theo dõi tiến độ tập luyện

---

## Yêu cầu hệ thống

### Phần mềm cần thiết:
-  Python 3.8 trở lên  (khuyến nghị Python 3.10 hoặc 3.11)
-  pip  (Python package manager)
-  Git  (tùy chọn, để clone repository)

### Phần cứng tối thiểu:
-  RAM : 4GB trở lên (khuyến nghị 8GB)
-  Ổ cứng : 2GB dung lượng trống
-  Internet : Cần kết nối để tải models lần đầu

### Tùy chọn (cho tính năng database):
-  Tài khoản Supabase  (miễn phí) - để lưu trữ dữ liệu người dùng

---

## Cài đặt

### Bước 1: Clone hoặc tải project

Nếu có Git:
```bash
git clone <repository-url>
cd "RAG GYM"
```

Hoặc tải và giải nén file ZIP vào thư mục `RAG GYM`.

### Bước 2: Kiểm tra Python

Mở Terminal/Command Prompt và kiểm tra phiên bản Python:

```bash
python --version
```

Hoặc:
```bash
python3 --version
```

Đảm bảo phiên bản >= 3.8.

### Bước 3: Tạo môi trường ảo (Khuyến nghị)

 Windows: 
```bash
python -m venv venv
venv\Scripts\activate
```

 Linux/Mac: 
```bash
python3 -m venv venv
source venv/bin/activate
```

### Bước 4: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

Lưu ý: Lần đầu cài đặt có thể mất 5-10 phút để tải các models và thư viện.

### Bước 5: Kiểm tra dataset

Đảm bảo file `data/megaGymDataset.csv` tồn tại trong thư mục project.

---

## Cấu hình

### Cấu hình cơ bản (Không bắt buộc)

Ứng dụng có thể chạy ngay mà không cần cấu hình thêm. Tuy nhiên, nếu muốn sử dụng tính năng lưu trữ dữ liệu người dùng, bạn cần cấu hình Supabase.

### Cấu hình Supabase (Tùy chọn)

1.  Tạo tài khoản Supabase: 
   - Truy cập [https://supabase.com](https://supabase.com)
   - Đăng ký tài khoản miễn phí
   - Tạo project mới

2.  Lấy thông tin API: 
   - Vào  Settings  →  API 
   - Copy  Project URL  và  anon public key 

3.  Tạo file `.env`: 
   - Copy file `env.example` thành `.env`
   - Điền thông tin:
   ```env
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-anon-public-key-here
   ```

4.  Setup Database Schema: 
   - Vào  SQL Editor  trong Supabase
   - Chạy SQL script từ file `database/FIX_SUPABASE_RLS.sql`
   - Hoặc tạo tables thủ công theo schema trong file đó

 Lưu ý:  Nếu không cấu hình Supabase, ứng dụng vẫn chạy được nhưng sẽ không lưu dữ liệu người dùng.

---

## Chạy ứng dụng

### Cách 1: Sử dụng script (Windows)

Double-click file `START.bat` hoặc chạy trong Command Prompt:

```bash
START.bat
```

### Cách 2: Chạy trực tiếp

```bash
python app.py
```

Hoặc:

```bash
python3 app.py
```

### Cách 3: Sử dụng uvicorn

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Truy cập ứng dụng

Sau khi chạy, mở trình duyệt và truy cập:

-  Web App : http://localhost:8000
-  Đăng nhập : http://localhost:8000/login
-  Đăng ký : http://localhost:8000/register
-  API Docs : http://localhost:8000/docs (Swagger UI)

---

## Sử dụng

### Chat với AI

1. Vào tab  Chat AI 
2. Gõ câu hỏi về gym (VD: "How to Chest Workout")
3. Nhấn Enter hoặc click  Gửi 
4. AI sẽ tìm kiếm và trả về các bài tập phù hợp

### Tạo Kế Hoạch Tập Luyện

1. Vào tab  Kế Hoạch Tập 
2. Điền thông tin:
   - Loại cơ thể (Ectomorph/Mesomorph/Endomorph)
   - Trình độ (Beginner/Intermediate/Advanced)
   - Mục tiêu (Tăng cơ/Giảm cân/Sức mạnh/Sức bền)
   - Số ngày tập/tuần (3-6 ngày)
   - Chiều cao, cân nặng, tuổi (tùy chọn)
   - Thiết bị có sẵn
3. Nhấn  Tạo Kế Hoạch Tập Luyện 
4. Xem kế hoạch chi tiết cho từng ngày

### Tìm Kiếm Bài Tập

1. Vào tab  Tìm Bài Tập 
2. Chọn bộ lọc:
   - Nhóm cơ (VD: Chest, Back)
   - Thiết bị (VD: Barbell, Dumbbell)
   - Trình độ
3. Nhấn  Tìm Kiếm 
4. Xem danh sách bài tập phù hợp

### Đăng nhập/Đăng ký (Nếu có Supabase)

1. Click  Đăng nhập  ở header
2. Nếu chưa có tài khoản, click  Đăng ký 
3. Điền form đăng ký (email, tên, thông tin thể chất)
4. Sau khi đăng nhập, dữ liệu sẽ tự động lưu vào database

---

## Cấu trúc dự án

```
RAG GYM/
├── app.py                      # FastAPI backend chính
├── rag_system_simple.py        # RAG system - xử lý AI
├── supabase_client.py          # Supabase client (nếu dùng database)
├── requirements.txt          # Dependencies Python
├── README.md                   # File này
├── START.bat                   # Script khởi chạy (Windows)
├── env.example                 # Template file cấu hình
│
├── data/                       # Dữ liệu
│   └── megaGymDataset.csv      # Dataset 2,920 bài tập
│
├── database/                   # Database scripts
│   └── FIX_SUPABASE_RLS.sql   # SQL schema cho Supabase
│
└── static/                     # Frontend files
    ├── index.html              # Trang chủ
    ├── auth.html               # Trang đăng nhập/đăng ký
    ├── styles.css              # CSS styling
    ├── script.js               # JavaScript logic
    ├── auth.css                # CSS cho auth page
    └── auth.js                 # JavaScript cho auth
```

---

## Công nghệ sử dụng

### Backend
-  FastAPI  (0.115.5) - Web framework hiện đại, hiệu năng cao
-  Uvicorn  (0.34.0) - ASGI server
-  Pydantic  (2.10.3) - Data validation

### AI & RAG
-  Sentence Transformers  (3.3.1) - Tạo embeddings
  - Model: `paraphrase-multilingual-mpnet-base-v2`
  - Hỗ trợ đa ngôn ngữ (Việt, Anh)
  - Embedding dimension: 768
-  Scikit-learn  - Cosine similarity cho semantic search
-  Pandas  (2.2.3) - Xử lý dữ liệu CSV
-  NumPy  (2.2.1) - Tính toán vectors

### Database (Tùy chọn)
-  Supabase  (2.10.0) - PostgreSQL database đám mây
-  python-dotenv  (1.0.0) - Quản lý environment variables

### Frontend
-  HTML5  - Semantic markup
-  CSS3  - Modern styling (Dark theme)
-  JavaScript (Vanilla)  - Logic xử lý

### Khác
-  Deep Translator  (1.11.4) - Dịch đa ngôn ngữ
-  aiofiles  (24.1.0) - Async file operations

### Dependencies đầy đủ

Xem file `requirements.txt` để biết phiên bản chi tiết của tất cả thư viện.

---

## API Documentation

### Core APIs

#### POST /api/chat
Chat với AI, tìm kiếm bài tập

 Request: 
```json
{
  "question": "How to Chest Workout",
  "n_results": 5,
  "user_id": "uuid-optional",
  "target": "vi"
}
```

 Response: 
```json
{
  "answer": "Dựa trên cơ sở dữ liệu...",
  "exercises": [
    {
      "title": "Bench Press",
      "bodypart": "Chest",
      "equipment": "Barbell",
      "level": "Beginner"
    }
  ]
}
```

#### POST /api/workout-plan
Tạo kế hoạch tập luyện

 Request: 
```json
{
  "body_type": "mesomorph",
  "fitness_level": "Intermediate",
  "goals": "muscle_gain",
  "days_per_week": 4,
  "height": 170,
  "weight": 70,
  "age": 25
}
```

#### POST /api/exercises/filter
Lọc bài tập

 Request: 
```json
{
  "body_part": "Chest",
  "equipment": "Barbell",
  "level": "Intermediate",
  "limit": 10
}
```

#### GET /api/statistics
Lấy thống kê dataset

#### GET /api/body-parts
Lấy danh sách nhóm cơ

#### GET /api/equipment
Lấy danh sách thiết bị

### User Management APIs (Cần Supabase)

- `POST /api/users` - Tạo user
- `GET /api/users/{user_id}` - Lấy thông tin user
- `PUT /api/users/{user_id}` - Cập nhật user
- `GET /api/users/{user_id}/workout-plans` - Lấy workout plans
- `GET /api/users/{user_id}/chat-history` - Lấy chat history
- `GET /api/users/{user_id}/favorites` - Lấy favorites
- `POST /api/users/{user_id}/favorites` - Thêm favorite
- `GET /api/users/{user_id}/progress` - Lấy progress

 Chi tiết đầy đủ:  Truy cập http://localhost:8000/docs sau khi chạy ứng dụng để xem Swagger UI.

---

## Troubleshooting

### Lỗi: ModuleNotFoundError

 Nguyên nhân:  Chưa cài đặt dependencies

 Giải pháp: 
```bash
pip install -r requirements.txt
```

### Lỗi: FileNotFoundError - megaGymDataset.csv

 Nguyên nhân:  File dataset không tồn tại

 Giải pháp:  Đảm bảo file `data/megaGymDataset.csv` có trong thư mục project

### Lỗi: Out of memory khi khởi động

 Nguyên nhân:  RAM không đủ để load embeddings

 Giải pháp: 
- Đóng các ứng dụng khác
- Tăng RAM (khuyến nghị 8GB+)
- Hoặc sử dụng máy có RAM lớn hơn

### Lỗi: Supabase connection failed

 Nguyên nhân:  Chưa cấu hình hoặc cấu hình sai

 Giải pháp: 
- Kiểm tra file `.env` có đúng format không
- Kiểm tra SUPABASE_URL và SUPABASE_KEY
- Ứng dụng vẫn chạy được, chỉ không lưu dữ liệu

### Lỗi: Port 8000 already in use

 Nguyên nhân:  Port 8000 đang được sử dụng

 Giải pháp: 
- Đóng ứng dụng đang chạy trên port 8000
- Hoặc thay đổi port trong `app.py`:
  ```python
  uvicorn.run(app, host="0.0.0.0", port=8001)
  ```

### Lần đầu chạy chậm

 Nguyên nhân:  Đang tải model Sentence Transformers

 Giải pháp:  Đây là bình thường, lần đầu sẽ mất 2-5 phút để tải model. Các lần sau sẽ nhanh hơn.

### Embeddings không được cache

 Nguyên nhân:  File cache bị lỗi hoặc không có quyền ghi

 Giải pháp:  Xóa file `embeddings_cache.pkl` và chạy lại, hệ thống sẽ tạo lại cache.

---

## Ghi chú

-  Dataset:  Dataset được lấy từ Kaggle - Mega Gym Dataset, chứa 2,920 bài tập với thông tin đầy đủ
-  Model:  Sử dụng `paraphrase-multilingual-mpnet-base-v2` - hỗ trợ tiếng Việt và tiếng Anh
-  Performance:  Tìm kiếm nhanh (< 1 giây) nhờ in-memory vector store
-  Database:  Supabase là tùy chọn, ứng dụng có thể chạy độc lập

---

## License

MIT License - Tự do sử dụng cho mục đích cá nhân và thương mại.

---

## Tác giả

Được xây dựng với Python

---

## Báo lỗi

Nếu gặp lỗi, vui lòng:
1. Kiểm tra Python version >= 3.8
2. Kiểm tra đã cài đủ dependencies
3. Kiểm tra file dataset có tồn tại
4. Xem logs trong terminal để biết lỗi chi tiết

---


