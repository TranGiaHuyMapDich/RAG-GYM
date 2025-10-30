# 📡 Hướng Dẫn Sử Dụng API với Supabase

## 🎯 Tổng Quan

Dự án đã được tích hợp đầy đủ với Supabase. Các API endpoints sẽ **TỰ ĐỘNG LƯU DỮ LIỆU** vào Supabase khi có `user_id`.

---

## 🔄 Cách Hoạt Động

### **Mode 1: Không có Supabase (Default)**
- Ứng dụng vẫn chạy bình thường
- Không lưu data vào database
- Chỉ trả về kết quả RAG

### **Mode 2: Có Supabase**
- Tự động lưu chat history, workout plans, favorites
- Lấy được lịch sử user
- Theo dõi tiến độ

---

## 📝 Endpoints Đã Được Cập Nhật

### 1. **POST `/api/chat`** - Chat với AI
**TỰ ĐỘNG LƯU** chat history nếu có `user_id`

**Request:**
```json
{
  "question": "Bài tập ngực cho người mới",
  "n_results": 5,
  "user_id": "uuid-của-user",      // Thêm để lưu vào Supabase
  "session_id": "uuid-session"     // Optional, auto-generate nếu không có
}
```

**Response:**
```json
{
  "answer": "...",
  "exercises": [...],
  "context": "..."
}
```

✅ **Đã lưu vào bảng `chat_history`**

---

### 2. **POST `/api/workout-plan`** - Tạo Kế Hoạch Tập
**TỰ ĐỘNG LƯU** workout plan nếu có `user_id`

**Request:**
```json
{
  "body_type": "mesomorph",
  "fitness_level": "Intermediate",
  "goals": "muscle_gain",
  "days_per_week": 4,
  "height": 170,
  "weight": 70,
  "age": 25,
  "user_id": "uuid-của-user",        // Thêm để lưu vào Supabase
  "plan_name": "4-Day Muscle Gain"   // Optional
}
```

**Response:**
```json
{
  "body_type": "mesomorph",
  "weekly_plan": [...],
  "recommendations": [...],
  "saved_plan_id": "uuid-of-saved-plan",
  "message": "✅ Kế hoạch đã được lưu vào database"
}
```

✅ **Đã lưu vào bảng `workout_plans`**

---

## 🆕 Endpoints Mới cho Supabase

### **USER MANAGEMENT**

#### **POST `/api/users`** - Tạo User Mới
```json
{
  "email": "user@example.com",
  "full_name": "Nguyễn Văn A",
  "body_type": "mesomorph",
  "fitness_level": "Intermediate",
  "height": 170,
  "weight": 70,
  "age": 25,
  "primary_goal": "muscle_gain",
  "available_equipment": ["Barbell", "Dumbbell"],
  "days_per_week": 4
}
```

Response:
```json
{
  "success": true,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    ...
  }
}
```

---

#### **GET `/api/users/{user_id}`** - Lấy Thông Tin User

Response:
```json
{
  "success": true,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "Nguyễn Văn A",
    "body_type": "mesomorph",
    ...
  }
}
```

---

#### **PUT `/api/users/{user_id}`** - Cập Nhật User

```json
{
  "weight": 72,
  "height": 171,
  "fitness_level": "Advanced"
}
```

---

### **WORKOUT PLANS**

#### **GET `/api/users/{user_id}/workout-plans`** - Lấy Tất Cả Plans của User

Response:
```json
{
  "success": true,
  "plans": [
    {
      "id": "uuid",
      "plan_name": "4-Day Split",
      "days_per_week": 4,
      "created_at": "2025-01-15T10:00:00",
      "plan_data": {...}
    }
  ]
}
```

---

#### **GET `/api/workout-plans/{plan_id}`** - Lấy Chi Tiết 1 Plan

Response:
```json
{
  "success": true,
  "plan": {
    "id": "uuid",
    "plan_name": "4-Day Split",
    "plan_data": {...},
    "created_at": "..."
  }
}
```

---

#### **DELETE `/api/workout-plans/{plan_id}`** - Xóa Plan

---

### **FAVORITE EXERCISES**

#### **POST `/api/users/{user_id}/favorites`** - Thêm Yêu Thích

```json
{
  "exercise_id": "123",
  "exercise_title": "Barbell Bench Press",
  "exercise_data": {
    "bodypart": "Chest",
    "equipment": "Barbell",
    "level": "Intermediate"
  },
  "notes": "Bài tập rất hiệu quả"
}
```

---

#### **GET `/api/users/{user_id}/favorites`** - Lấy Danh Sách Yêu Thích

Response:
```json
{
  "success": true,
  "favorites": [
    {
      "id": "uuid",
      "exercise_id": "123",
      "exercise_title": "Barbell Bench Press",
      "exercise_data": {...},
      "personal_notes": "...",
      "times_performed": 5,
      "created_at": "..."
    }
  ]
}
```

---

#### **DELETE `/api/users/{user_id}/favorites/{exercise_id}`** - Xóa Khỏi Yêu Thích

---

### **CHAT HISTORY**

#### **GET `/api/users/{user_id}/chat-history`** - Lấy Lịch Sử Chat

Query params:
- `session_id` (optional): Filter theo session
- `limit` (optional, default 50): Giới hạn số records

Response:
```json
{
  "success": true,
  "history": [
    {
      "id": "uuid",
      "user_message": "Bài tập ngực cho người mới",
      "ai_response": "...",
      "exercises_suggested": [...],
      "created_at": "..."
    }
  ]
}
```

---

### **PROGRESS TRACKING**

#### **POST `/api/users/{user_id}/progress`** - Thêm Entry Tiến Độ

```json
{
  "weight": 72.5,
  "body_fat_percentage": 15.2,
  "notes": "Cảm thấy khỏe hơn",
  "measurement_date": "2025-01-15"
}
```

---

#### **GET `/api/users/{user_id}/progress`** - Lấy Lịch Sử Tiến Độ

Query params:
- `limit` (optional, default 30)

Response:
```json
{
  "success": true,
  "progress": [
    {
      "id": "uuid",
      "weight": 72.5,
      "body_fat_percentage": 15.2,
      "measurement_date": "2025-01-15",
      "created_at": "..."
    }
  ]
}
```

---

### **STATISTICS**

#### **GET `/api/users/{user_id}/stats`** - Lấy Thống Kê User

Response:
```json
{
  "success": true,
  "stats": {
    "total_plans": 3,
    "total_favorites": 10,
    "total_sessions": 0,
    "latest_weight": 72.5,
    "latest_measurement_date": "2025-01-15"
  }
}
```

---

## 🔄 Workflow Ví Dụ

### **Workflow 1: User mới đăng ký**

```javascript
// 1. Tạo user
const createUserResponse = await fetch('/api/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'newuser@gym.com',
    full_name: 'Nguyễn Văn A',
    body_type: 'mesomorph',
    fitness_level: 'Beginner',
    height: 170,
    weight: 70,
    age: 25,
    primary_goal: 'muscle_gain'
  })
});

const { user } = await createUserResponse.json();
const userId = user.id;

// 2. Tạo workout plan
const planResponse = await fetch('/api/workout-plan', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    body_type: 'mesomorph',
    fitness_level: 'Beginner',
    goals: 'muscle_gain',
    days_per_week: 3,
    user_id: userId,  // ← Quan trọng!
    plan_name: 'My First Plan'
  })
});

const plan = await planResponse.json();
console.log('Plan saved:', plan.saved_plan_id);

// 3. Chat với AI
const chatResponse = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'Bài tập ngực cho người mới',
    user_id: userId  // ← Tự động lưu chat
  })
});
```

---

### **Workflow 2: User quay lại**

```javascript
const userId = 'existing-user-uuid';

// 1. Lấy thông tin user
const user = await fetch(`/api/users/${userId}`).then(r => r.json());

// 2. Lấy workout plans đã lưu
const plans = await fetch(`/api/users/${userId}/workout-plans`).then(r => r.json());

// 3. Lấy lịch sử chat
const history = await fetch(`/api/users/${userId}/chat-history?limit=20`).then(r => r.json());

// 4. Xem tiến độ
const progress = await fetch(`/api/users/${userId}/progress`).then(r => r.json());

// 5. Xem stats
const stats = await fetch(`/api/users/${userId}/stats`).then(r => r.json());
```

---

## ⚙️ Cấu Hình

### **Kiểm tra Supabase có hoạt động không:**

```javascript
// Frontend - check server status
const response = await fetch('/api/statistics');
if (response.ok) {
  console.log('Server OK');
}
```

### **Xử lý khi Supabase không available:**

Ứng dụng sẽ vẫn chạy bình thường, chỉ không lưu data:
- Chat vẫn hoạt động (không lưu history)
- Workout plan vẫn tạo được (không lưu vào DB)
- Tất cả endpoints Supabase sẽ trả về 503

---

## 📊 Data Flow

```
User Request
    ↓
FastAPI Endpoint
    ↓
RAG System (AI Processing)
    ↓
Generate Response
    ↓
[IF user_id provided]
    ↓
Save to Supabase
    ↓
Return Response + Saved Info
```

---

## 🔐 Bảo Mật

- ✅ Row Level Security (RLS) enabled
- ✅ Users chỉ xem được data của mình
- ✅ API key chỉ dùng `anon` key
- ❌ Chưa có authentication (cần implement Supabase Auth)

---

## 🎯 Next Steps

1. **Implement Frontend Integration**
   - Thêm user login/register
   - Lưu user_id vào localStorage
   - Hiển thị saved plans, favorites

2. **Add Supabase Auth**
   - Implement đăng ký/đăng nhập
   - OAuth providers (Google, Facebook)
   - Protected routes

3. **Enhance Features**
   - Workout sessions tracking
   - Progress charts
   - Social features

---

## ✅ Checklist Triển Khai

- [ ] Tạo project Supabase
- [ ] Chạy SQL schema
- [ ] Lấy API keys
- [ ] Tạo file `.env`
- [ ] Test create user
- [ ] Test save workout plan
- [ ] Test chat history
- [ ] Integrate vào frontend

---

**🎉 Hoàn Thành! Dự án đã sẵn sàng với Supabase!**

