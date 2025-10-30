# 📱 HƯỚNG DẪN SỬ DỤNG TÍNH NĂNG USER - FRONTEND

## 🎯 **TỔNG QUAN**

Frontend đã được **tích hợp đầy đủ** với Supabase Database! Bây giờ bạn có thể:

✅ Đăng ký/Đăng nhập user  
✅ Tự động lưu chat history  
✅ Tự động lưu workout plans  
✅ Xem lại dữ liệu đã lưu  
✅ Quản lý favorites (coming soon)  

---

## 🚀 **CÁCH SỬ DỤNG**

### **1. Khi Chưa Đăng Nhập**

**Trạng thái:**
```
⚠️ Chưa đăng nhập (dữ liệu không được lưu)
[Đăng ký nhanh]
```

**Hoạt động:**
- ✅ Vẫn chat bình thường
- ✅ Vẫn tạo workout plan
- ❌ Chat history KHÔNG lưu
- ❌ Workout plans KHÔNG lưu

---

### **2. Đăng Ký Nhanh**

**Cách 1: Qua UI (Khuyến nghị)**

1. Click nút **"Đăng ký nhanh"** ở header
2. Nhập email (ví dụ: `myemail@gmail.com`)
3. Nhập tên (ví dụ: `Nguyễn Văn A`)
4. Nhận thông báo: ✅ Đăng ký thành công!

**Cách 2: Qua Browser Console (F12)**

```javascript
// Tạo user mới
fetch('http://localhost:8000/api/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'test@gym.com',
    full_name: 'Test User',
    body_type: 'mesomorph',
    fitness_level: 'Intermediate',
    primary_goal: 'muscle_gain'
  })
})
.then(r => r.json())
.then(data => {
  console.log('✅ User ID:', data.user.id);
  localStorage.setItem('userId', data.user.id);
  location.reload(); // Tải lại trang
});
```

---

### **3. Khi Đã Đăng Nhập**

**Trạng thái:**
```
✅ Đã đăng nhập
[Đăng xuất] [Dữ liệu của tôi]
```

**Hoạt động:**
- ✅ Chat → Auto lưu vào `chat_history`
- ✅ Tạo workout plan → Auto lưu vào `workout_plans`
- ✅ Nhận notification khi lưu thành công
- ✅ Xem lại data đã lưu

---

### **4. Xem Dữ Liệu Đã Lưu**

Click nút **"Dữ liệu của tôi"** để xem:

**Hiển thị:**
```
📊 Dữ Liệu Của Bạn

┌─────────────────┬────────────────────┐
│   5 Plans       │   12 Favorites     │
│ Kế hoạch tập    │ Bài tập yêu thích  │
└─────────────────┴────────────────────┘

📋 Kế hoạch đã lưu:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Plan 21/10/2025
4 ngày/tuần - 21/10/2025
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Plan 20/10/2025
3 ngày/tuần - 20/10/2025
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔄 **LUỒNG HOẠT ĐỘNG**

### **Chat Flow:**

```
User nhập câu hỏi
    ↓
Frontend gửi request:
{
  question: "Bài tập ngực",
  user_id: "uuid",      ← Auto thêm nếu đã login
  session_id: "uuid"    ← Auto thêm
}
    ↓
Backend xử lý RAG
    ↓
Nếu có user_id → Lưu vào Supabase
    ↓
Trả về response
    ↓
Frontend hiển thị
```

### **Workout Plan Flow:**

```
User điền form
    ↓
Frontend gửi request:
{
  body_type: "mesomorph",
  fitness_level: "Intermediate",
  goals: "muscle_gain",
  user_id: "uuid",      ← Auto thêm nếu đã login
  plan_name: "Plan 21/10/2025"
}
    ↓
Backend tạo plan
    ↓
Nếu có user_id → Lưu vào Supabase
    ↓
Trả về plan + saved_plan_id
    ↓
Frontend hiển thị + notification
```

---

## 🎨 **TÍNH NĂNG MỚI TRONG FRONTEND**

### **1. User Status Bar**
- Hiển thị trạng thái đăng nhập
- Nút đăng ký/đăng xuất
- Nút xem dữ liệu

### **2. Auto-Save Notifications**
- Toast notification khi lưu thành công
- Hiển thị trong 3 giây
- 4 loại: success, error, warning, info

### **3. Data Viewer Modal**
- Popup modal hiển thị data
- Stats cards (plans, favorites)
- List workout plans
- Scroll nếu nhiều data

### **4. LocalStorage Management**
```javascript
// Lưu user_id
localStorage.setItem('userId', 'uuid');

// Lưu session_id
localStorage.setItem('sessionId', 'uuid');

// Lấy ra
const userId = localStorage.getItem('userId');
```

### **5. Session Management**
- Mỗi lần mở app = 1 session mới
- Session ID tự động tạo
- Chat history được nhóm theo session

---

## 🔧 **CÁC HÀM JAVASCRIPT MỚI**

### **User Management:**

```javascript
// Đăng ký user mới
async function quickRegister()

// Set user ID
function setUserId(userId)

// Đăng xuất
function logout()

// Cập nhật trạng thái UI
function updateUserStatus()
```

### **Data Viewer:**

```javascript
// Xem data của user
async function viewMyData()

// Đóng modal
function closeMyData()
```

### **Notifications:**

```javascript
// Hiển thị thông báo
showNotification(message, type)

// Types: 'success', 'error', 'warning', 'info'
```

### **Utilities:**

```javascript
// Tạo UUID
function generateUUID()
```

---

## 📊 **DỮ LIỆU ĐƯỢC LƯU**

### **Chat History:**
```javascript
{
  user_id: "uuid",
  session_id: "uuid",
  user_message: "Bài tập ngực cho newbie",
  ai_response: "Đây là các bài tập...",
  exercises_suggested: [...],
  context_used: "..."
}
```

### **Workout Plans:**
```javascript
{
  user_id: "uuid",
  plan_name: "Plan 21/10/2025",
  body_type: "mesomorph",
  fitness_level: "Intermediate",
  primary_goal: "muscle_gain",
  days_per_week: 4,
  plan_data: {
    weekly_schedule: [...],
    bmi: 22.5,
    exercises: [...]
  }
}
```

---

## 🎯 **DEMO SCENARIOS**

### **Scenario 1: User Mới**

1. Mở app lần đầu
2. Thấy: "⚠️ Chưa đăng nhập (dữ liệu không được lưu)"
3. Click "Đăng ký nhanh"
4. Nhập email + tên
5. Thấy: "✅ Đã đăng nhập"
6. Chat/tạo plan → Tự động lưu
7. Click "Dữ liệu của tôi" → Thấy data

### **Scenario 2: User Quay Lại**

1. Mở app
2. LocalStorage có user_id
3. Tự động: "✅ Đã đăng nhập"
4. Tiếp tục chat/tạo plan
5. Data tiếp tục được lưu

### **Scenario 3: Không Có Supabase**

1. Mở app (chưa config Supabase)
2. Thấy: "⚠️ Chưa đăng nhập"
3. Click "Đăng ký nhanh"
4. Thấy: "❌ Lỗi kết nối. Supabase chưa được cấu hình."
5. App vẫn hoạt động bình thường, chỉ không lưu

---

## 🔐 **BẢO MẬT**

### **LocalStorage:**
- User ID được lưu trong localStorage
- Không lưu password/token nhạy cảm
- Clear khi logout

### **Session:**
- Mỗi tab = 1 session ID riêng
- Session ID random UUID
- Không liên quan đến security

### **API Calls:**
- Tất cả qua HTTPS (production)
- User ID gửi trong request body
- Backend validate qua Supabase RLS

---

## 🚀 **NEXT STEPS**

### **Tính Năng Sắp Tới:**

1. **Favorite Exercises**
   - ⭐ Button trên mỗi exercise
   - Lưu vào `favorite_exercises`
   - Xem lại trong "Dữ liệu của tôi"

2. **Progress Tracking**
   - 📈 Nhập cân nặng/body fat
   - Chart hiển thị tiến độ
   - Lưu vào `progress_tracking`

3. **Supabase Authentication**
   - 🔐 Login/Register với password
   - Email verification
   - Social login (Google, Facebook)

4. **Advanced User Profile**
   - Ảnh đại diện
   - Chỉnh sửa thông tin
   - Preferences/Settings

---

## 💡 **TIPS**

### **Để Test:**
```javascript
// Check current user
console.log('User ID:', localStorage.getItem('userId'));

// Manual set user (for testing)
localStorage.setItem('userId', 'your-uuid-here');
location.reload();

// Clear all data
localStorage.clear();
location.reload();
```

### **Debug:**
```javascript
// Xem tất cả localStorage
for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    console.log(key, localStorage.getItem(key));
}
```

---

## 📞 **SUPPORT**

Nếu gặp vấn đề:

1. Check browser console (F12)
2. Check Network tab (xem API calls)
3. Check Supabase dashboard (data có lưu không)
4. Clear localStorage và thử lại

---

**✨ Tận hưởng trải nghiệm Gym AI với data persistence! 💪**

