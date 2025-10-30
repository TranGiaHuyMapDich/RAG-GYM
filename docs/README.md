# 🏋️ Gym RAG AI Assistant - Trợ Lý Gym Thông Minh

Hệ thống RAG (Retrieval Augmented Generation) AI thông minh dành cho gym, sử dụng hơn **2900+ bài tập** từ dataset để cung cấp tư vấn tập luyện cá nhân hóa.

🆕 **Version 2.1** - Tích hợp đầy đủ với Supabase Database cho data persistence!  
🔐 **NEW!** - Trang đăng nhập/đăng ký chuyên nghiệp với UI hiện đại!

## ✨ Tính Năng

### 💬 Chat AI Thông Minh
- Hỏi đáp về bài tập gym, kỹ thuật, dinh dưỡng
- Tìm kiếm bài tập theo ngữ nghĩa (semantic search)
- Gợi ý bài tập phù hợp với từng nhóm cơ

### 📋 Kế Hoạch Tập Luyện Cá Nhân Hóa
- Phân tích theo **loại cơ thể** (Ectomorph, Mesomorph, Endomorph)
- Tùy chỉnh theo **trình độ** (Beginner, Intermediate, Advanced)
- Đặt **mục tiêu** (Tăng cơ, Giảm cân, Tăng sức mạnh, Sức bền)
- Tính toán **BMI** và đưa ra lời khuyên
- Tạo lịch tập **3-6 ngày/tuần**
- Lọc theo **thiết bị có sẵn**

### 🔍 Tìm Kiếm Bài Tập
- Lọc theo nhóm cơ (Chest, Back, Shoulders, Legs, v.v.)
- Lọc theo thiết bị (Barbell, Dumbbell, Machine, v.v.)
- Lọc theo cấp độ
- Xem rating và mô tả chi tiết

### 📊 Thống Kê Dataset
- Tổng quan về số lượng bài tập
- Phân bố theo nhóm cơ, thiết bị, cấp độ
- Top bài tập phổ biến

### 🆕 User Management & Data Persistence
- 🔐 **Trang đăng nhập/đăng ký** chuyên nghiệp với UI đẹp
- **Đăng ký** với form đầy đủ (email, tên, thông tin thể chất, mục tiêu)
- **Đăng nhập** nhanh bằng email
- **Remember me** - Ghi nhớ đăng nhập
- **Tự động lưu** chat history vào database
- **Tự động lưu** workout plans đã tạo
- **Xem lại** dữ liệu đã lưu (plans, favorites, chat history)
- **Thống kê cá nhân** (số plans, favorites, v.v.)
- **Theo dõi tiến độ** tập luyện
- Tích hợp **Supabase** (PostgreSQL + Real-time)

## 🚀 Công Nghệ Sử Dụng

- **Backend**: FastAPI (Python web framework)
- **RAG Engine**: In-memory vector search với Sentence Transformers
- **Embeddings**: Sentence Transformers (paraphrase-multilingual-mpnet-base-v2)
- **Database**: Supabase (PostgreSQL + Real-time)
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **User Management**: LocalStorage + Supabase Auth-ready

## 📦 Cài Đặt

### Yêu Cầu Hệ Thống
- Python 3.8 trở lên
- 4GB RAM trở lên (để chạy embeddings model)
- 2GB dung lượng ổ cứng

### Bước 1: Clone hoặc tải project
```bash
cd "RAG GYM"
```

### Bước 2: Cài đặt dependencies

**Option A - Chạy nhanh (Không database):**
```bash
python -m pip install -r requirements_simple.txt
```

**Option B - Đầy đủ tính năng (Có database):**
```bash
python -m pip install -r requirements_simple.txt
python -m pip install supabase python-dotenv
```

**Lưu ý**: Lần đầu tiên cài đặt có thể mất 5-10 phút để tải các models.

### Bước 3: Cấu hình Database (Tùy chọn)

**Nếu muốn lưu dữ liệu (chat history, workout plans):**

1. Tạo project trên [Supabase](https://supabase.com)
2. Tạo tables (copy SQL từ `QUICK_SUPABASE_SETUP.txt`)
3. Tạo file `.env`:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

**Chi tiết:** Xem `QUICKSTART_WITH_DATABASE.md`

### Bước 4: Chạy ứng dụng

#### Windows:
```bash
python app.py
```

Hoặc sử dụng script khởi chạy:
```bash
python start.py
```

#### Linux/Mac:
```bash
python3 app.py
```

### Bước 5: Truy cập ứng dụng
Mở trình duyệt và truy cập:
- **Web App**: http://localhost:8000
- **🔐 Đăng Nhập**: http://localhost:8000/login
- **🆕 Đăng Ký**: http://localhost:8000/register
- **API Docs**: http://localhost:8000/docs
- **Test User Features**: http://localhost:8000/test_user_features.html

## 📖 Hướng Dẫn Sử Dụng

### 🔐 Đăng Nhập/Đăng Ký (Mới!)
**Đăng ký:**
1. Vào **http://localhost:8000/register** hoặc click "Đăng Ký" ở header
2. Điền form (email, tên, thông tin thể chất, mục tiêu)
3. Click **"Tạo Tài Khoản"**
4. Tự động redirect về trang chính → **✅ Đã đăng nhập**

**Đăng nhập:**
1. Vào **http://localhost:8000/login** hoặc click "Đăng Nhập" ở header
2. Nhập email đã đăng ký
3. (Optional) Check "Ghi nhớ đăng nhập"
4. Click **"Đăng Nhập"**
5. Tự động redirect về trang chính → **✅ Đã đăng nhập**

### Chat với AI Assistant
1. Vào tab **💬 Chat AI**
2. Gõ câu hỏi về gym (VD: "Bài tập ngực cho người mới bắt đầu")
3. AI sẽ tìm kiếm và trả về các bài tập phù hợp nhất
4. **Nếu đã đăng nhập**: Chat history tự động lưu vào database!

### Tạo Kế Hoạch Tập Luyện
1. Vào tab **📋 Kế Hoạch Tập**
2. Điền thông tin:
   - Loại cơ thể (Ectomorph/Mesomorph/Endomorph)
   - Trình độ (Beginner/Intermediate/Advanced)
   - Mục tiêu (Tăng cơ/Giảm cân/Sức mạnh/Sức bền)
   - Số ngày tập/tuần (3-6 ngày)
   - Chiều cao, cân nặng, tuổi (tùy chọn)
   - Thiết bị có sẵn
3. Nhấn **🚀 Tạo Kế Hoạch Tập Luyện**
4. Xem kế hoạch chi tiết cho từng ngày
5. **Nếu đã đăng nhập**: Plan tự động lưu vào database!

### Tìm Kiếm Bài Tập
1. Vào tab **🔍 Tìm Bài Tập**
2. Chọn bộ lọc:
   - Nhóm cơ (VD: Chest, Back)
   - Thiết bị (VD: Barbell, Dumbbell)
   - Trình độ
3. Nhấn **🔍 Tìm Kiếm**
4. Xem danh sách bài tập phù hợp

### 🆕 Xem Dữ Liệu Đã Lưu
1. Click nút **"Dữ liệu của tôi"** ở header
2. Xem:
   - 📊 Thống kê (số plans, favorites)
   - 📋 Danh sách workout plans đã tạo
   - ⭐ Bài tập yêu thích
   - 💬 Lịch sử chat

## 🎯 Các Loại Cơ Thể

### Ectomorph (Người gầy, khó tăng cân)
- **Đặc điểm**: Khó tăng cân và cơ bắp
- **Khuyến nghị**: 
  - Tập trọng lượng nặng, ít cardio
  - Số lần lặp lại thấp (6-8 reps)
  - Ăn nhiều protein và carbs

### Mesomorph (Người cơ bắp, dễ tăng cơ)
- **Đặc điểm**: Dễ tăng cơ và giảm mỡ
- **Khuyến nghị**:
  - Cân bằng giữa cardio và tập sức mạnh
  - Số lần lặp lại trung bình (8-12 reps)
  - Đa dạng các bài tập

### Endomorph (Người dễ tăng cân)
- **Đặc điểm**: Dễ tích mỡ, cần kiểm soát calo
- **Khuyến nghị**:
  - Kết hợp nhiều cardio và HIIT
  - Số lần lặp lại cao (12-15 reps)
  - Tập circuit training

## 📊 Dataset

Dataset chứa **2920 bài tập** với các thông tin:
- **Title**: Tên bài tập
- **Description**: Mô tả chi tiết
- **Type**: Loại bài tập (Strength, Cardio, etc.)
- **BodyPart**: Nhóm cơ (Chest, Back, Legs, etc.)
- **Equipment**: Thiết bị cần thiết
- **Level**: Cấp độ (Beginner/Intermediate/Advanced)
- **Rating**: Đánh giá chất lượng

## 🔧 API Endpoints

### Core RAG APIs

#### POST /api/chat
Hỏi đáp với AI (Auto-save nếu có user_id)
```json
{
  "question": "Bài tập ngực cho người mới bắt đầu",
  "n_results": 5,
  "user_id": "uuid",      // Optional - để auto-save
  "session_id": "uuid"    // Optional
}
```

#### POST /api/workout-plan
Tạo kế hoạch tập luyện (Auto-save nếu có user_id)
```json
{
  "body_type": "mesomorph",
  "fitness_level": "Intermediate",
  "goals": "muscle_gain",
  "available_equipment": ["Barbell", "Dumbbell"],
  "days_per_week": 4,
  "height": 170,
  "weight": 70,
  "age": 25,
  "user_id": "uuid",      // Optional - để auto-save
  "plan_name": "Plan 21/10/2025"  // Optional
}
```

### 🆕 User Management APIs

#### POST /api/users
Tạo user mới
```json
{
  "email": "user@example.com",
  "full_name": "Nguyễn Văn A",
  "body_type": "mesomorph",
  "fitness_level": "Intermediate",
  "primary_goal": "muscle_gain"
}
```

#### GET /api/users/{user_id}
Lấy thông tin user

#### PUT /api/users/{user_id}
Cập nhật thông tin user

#### GET /api/users/{user_id}/stats
Lấy thống kê user (tổng plans, favorites, v.v.)

#### GET /api/users/{user_id}/workout-plans
Lấy danh sách workout plans đã lưu

#### GET /api/users/{user_id}/chat-history
Lấy lịch sử chat

**Chi tiết đầy đủ:** Xem `SUPABASE_API_GUIDE.md`

### POST /api/exercises/filter
Lọc bài tập
```json
{
  "body_part": "Chest",
  "equipment": "Barbell",
  "level": "Intermediate",
  "limit": 10
}
```

### GET /api/statistics
Lấy thống kê dataset

### GET /api/body-parts
Lấy danh sách nhóm cơ

### GET /api/equipment
Lấy danh sách thiết bị

## 🧠 Cách Hoạt Động của RAG

1. **Embedding**: Chuyển đổi text thành vectors sử dụng Sentence Transformers
2. **Vector Store**: Lưu trữ vectors trong memory (nhanh, không cần database phức tạp)
3. **Semantic Search**: Tìm kiếm theo ngữ nghĩa, không phải từ khóa
4. **Retrieval**: Lấy top K documents liên quan nhất (cosine similarity)
5. **Response**: Trả về kết quả cho người dùng
6. **🆕 Auto-Save**: Nếu user đã login, tự động lưu vào Supabase

## 🎨 Giao Diện

- **Modern UI**: Thiết kế hiện đại với gradient colors
- **Responsive**: Tương thích với mobile và desktop
- **Dark Theme**: Giao diện tối, dễ nhìn
- **Smooth Animations**: Hiệu ứng mượt mà
- **🆕 User Status Bar**: Hiển thị trạng thái đăng nhập
- **🆕 Toast Notifications**: Thông báo khi lưu dữ liệu
- **🆕 Data Viewer Modal**: Xem dữ liệu đã lưu đẹp mắt

## 🤝 Đóng Góp

Mọi đóng góp đều được hoan nghênh! Hãy:
1. Fork project
2. Tạo branch mới
3. Commit changes
4. Push và tạo Pull Request

## 📝 License

MIT License - Tự do sử dụng cho mục đích cá nhân và thương mại.

## 👨‍💻 Tác Giả

Được xây dựng với ❤️ và Python

## 🐛 Báo Lỗi

Nếu gặp lỗi, vui lòng:
1. Kiểm tra Python version >= 3.8 (khuyến nghị 3.11)
2. Kiểm tra đã cài đủ dependencies
3. Kiểm tra file `megaGymDataset.csv` có trong thư mục
4. Xem logs trong terminal
5. **Nếu lỗi Supabase**: App vẫn chạy được, chỉ không lưu data

## 📚 Documentation

**Getting Started:**
- **`START_HERE.txt`** - Bắt đầu từ đây!
- **`LOGIN_GUIDE.txt`** - 🔐 Hướng dẫn đăng nhập/đăng ký (MỚI!)
- **`INTEGRATION_COMPLETE.txt`** - Tổng kết version 2.1

**User Features:**
- **`AUTH_SYSTEM_GUIDE.md`** - 🔐 Chi tiết hệ thống auth (MỚI!)
- **`FRONTEND_USER_GUIDE.md`** - Chi tiết tính năng user management
- **`WHATS_NEW.md`** - Version 2.0+ features

**Setup & API:**
- **`QUICKSTART_WITH_DATABASE.md`** - Hướng dẫn setup nhanh với database
- **`SUPABASE_API_GUIDE.md`** - API documentation đầy đủ
- **`QUICK_SUPABASE_SETUP.txt`** - Setup Supabase từng bước
- **`API_DOCUMENTATION.md`** - Tổng hợp API endpoints

**Technical:**
- **`HOW_IT_WORKS.txt`** - Diagrams hệ thống
- **`RUNNING_GUIDE.md`** - Hướng dẫn chạy ứng dụng

## 📞 Liên Hệ

Có câu hỏi? Hãy mở issue trên GitHub!

---

**💪 Chúc bạn tập luyện hiệu quả với Gym RAG AI Assistant!**

