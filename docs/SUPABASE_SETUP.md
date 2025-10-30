# 🔧 Hướng Dẫn Cấu Hình Supabase

## 📋 Bước 1: Tạo Project trên Supabase

1. Truy cập: https://app.supabase.com
2. Click **"New Project"**
3. Điền thông tin:
   - **Name**: Gym RAG AI
   - **Database Password**: Tạo password mạnh
   - **Region**: Southeast Asia (Singapore) - gần VN nhất
4. Click **"Create new project"**
5. Đợi 2-3 phút để Supabase setup

---

## 🗄️ Bước 2: Tạo Database Schema

1. Vào **SQL Editor** (sidebar bên trái)
2. Click **"New Query"**
3. Copy toàn bộ code SQL này và paste vào:

```sql
-- Enable UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table: users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    body_type TEXT,
    fitness_level TEXT,
    height DECIMAL(5,2),
    weight DECIMAL(5,2),
    age INTEGER,
    primary_goal TEXT,
    available_equipment JSONB,
    days_per_week INTEGER DEFAULT 3,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: workout_plans
CREATE TABLE workout_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    plan_name TEXT NOT NULL,
    plan_data JSONB NOT NULL,
    is_favorite BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: favorite_exercises
CREATE TABLE favorite_exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    exercise_id TEXT NOT NULL,
    exercise_title TEXT NOT NULL,
    exercise_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, exercise_id)
);

-- Table: chat_history
CREATE TABLE chat_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID DEFAULT uuid_generate_v4(),
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    exercises_suggested JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: progress_tracking
CREATE TABLE progress_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    weight DECIMAL(5,2),
    body_fat_percentage DECIMAL(4,2),
    notes TEXT,
    measurement_date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, measurement_date)
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_workout_plans_user ON workout_plans(user_id);
CREATE INDEX idx_favorites_user ON favorite_exercises(user_id);
CREATE INDEX idx_chat_user ON chat_history(user_id);
CREATE INDEX idx_progress_user ON progress_tracking(user_id);

-- RLS Policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE workout_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE favorite_exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE progress_tracking ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users view own data" ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users update own data" ON users FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users manage own plans" ON workout_plans FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users manage own favorites" ON favorite_exercises FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users manage own chat" ON chat_history FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users manage own progress" ON progress_tracking FOR ALL USING (auth.uid() = user_id);
```

4. Click **RUN** hoặc nhấn `Ctrl + Enter`
5. Kiểm tra **Table Editor** để xem các bảng đã tạo

---

## 🔑 Bước 3: Lấy API Keys

1. Vào **Settings** → **API**
2. Copy 2 thông tin sau:

### **Project URL**
```
https://abcdefghijk.supabase.co
```
Copy URL này

### **API Key (anon/public)**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
Copy key `anon` `public` (key dài)

---

## 📝 Bước 4: Cấu Hình trong Dự Án

### 4.1. Tạo file `.env`

Trong thư mục dự án, tạo file mới tên `.env`:

```env
SUPABASE_URL=https://abcdefghijk.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Thay thế:**
- `https://abcdefghijk.supabase.co` → Project URL của bạn
- `eyJhbG...` → API Key (anon) của bạn

### 4.2. Cài đặt thêm packages

```bash
python -m pip install supabase python-dotenv
```

---

## ✅ Bước 5: Test Kết Nối

Chạy lệnh test:

```bash
python supabase_client.py
```

Nếu thấy: `✅ Connected to Supabase successfully!` → Thành công!

---

## 🎯 Sử Dụng Supabase trong Code

### Import và khởi tạo:

```python
from supabase_client import get_supabase_manager

sb = get_supabase_manager()
```

### Ví dụ: Tạo user mới

```python
user_data = {
    "email": "user@example.com",
    "full_name": "Nguyễn Văn A",
    "body_type": "mesomorph",
    "fitness_level": "Intermediate",
    "primary_goal": "muscle_gain",
    "height": 170,
    "weight": 70,
    "age": 25
}

result = sb.create_user(user_data)
print(result)
```

### Ví dụ: Lưu workout plan

```python
plan_data = {
    "plan_name": "4-Day Muscle Gain",
    "body_type": "mesomorph",
    "fitness_level": "Intermediate",
    "goals": "muscle_gain",
    "days_per_week": 4,
    "weekly_plan": [...],  # Data từ RAG
}

result = sb.save_workout_plan(user_id="user-uuid", plan_data=plan_data)
print(result)
```

### Ví dụ: Lưu chat history

```python
result = sb.save_chat(
    user_id="user-uuid",
    session_id="session-uuid",
    user_message="Bài tập ngực cho người mới",
    ai_response="Đây là các bài tập...",
    exercises_suggested=[...],  # List exercises
)
```

---

## 🔐 Bảo Mật

### **QUAN TRỌNG:**
- ❌ **KHÔNG** commit file `.env` lên Git
- ✅ File `.env` đã được thêm vào `.gitignore`
- ✅ Chỉ dùng `anon key` cho client-side
- ✅ Dùng `service_role key` cho admin operations (cẩn thận!)

---

## 📊 Quản Lý Data

### Xem data trong Supabase:
1. Vào **Table Editor**
2. Click vào table muốn xem (users, workout_plans, etc.)
3. Xem, thêm, sửa, xóa data trực tiếp

### Query SQL:
1. Vào **SQL Editor**
2. Viết query, VD:
```sql
SELECT * FROM users WHERE fitness_level = 'Intermediate';
```

---

## ❓ Troubleshooting

### Lỗi: "Missing SUPABASE_URL"
→ Kiểm tra file `.env` đã tạo chưa và có đúng format không

### Lỗi: "Invalid API key"
→ Kiểm tra lại API key, đảm bảo copy đúng key `anon public`

### Lỗi: "Row Level Security"
→ Đảm bảo đã chạy SQL tạo policies ở Bước 2

### Không kết nối được
→ Kiểm tra internet, project Supabase đã active chưa

---

## 🎉 Hoàn Thành!

Bạn đã sẵn sàng sử dụng Supabase trong dự án Gym RAG AI!

**Next Steps:**
- Tích hợp vào frontend để save/load user data
- Thêm authentication (Supabase Auth)
- Track user progress over time

