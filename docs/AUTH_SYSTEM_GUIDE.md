# 🔐 HƯỚNG DẪN HỆ THỐNG ĐĂNG NHẬP/ĐĂNG KÝ

## ✨ **TỔNG QUAN**

Gym RAG AI bây giờ có trang đăng nhập/đăng ký chuyên nghiệp!

### **Tính Năng:**
- ✅ Trang login/register đẹp với UI hiện đại
- ✅ Form đăng ký đầy đủ (email, tên, thông tin thể chất, mục tiêu)
- ✅ Login bằng email
- ✅ Remember me
- ✅ Auto redirect sau khi login/register
- ✅ Validation đầy đủ
- ✅ Toast notifications
- ✅ Loading states
- ✅ Responsive design

---

## 🎨 **UI COMPONENTS**

### **Trang Auth:**
- 📄 File: `static/auth.html`
- 🎨 CSS: `static/auth.css`
- 💻 JS: `static/auth.js`

### **Features:**
```
┌─────────────────────────────────────┐
│         🏋️ Gym RAG AI               │
│   Trợ lý gym thông minh với AI      │
├─────────────────────────────────────┤
│  [Đăng Nhập]  [Đăng Ký]   ← Tabs   │
├─────────────────────────────────────┤
│                                     │
│  📧 Email                           │
│  [________________]                 │
│                                     │
│  ☑️ Ghi nhớ đăng nhập               │
│                                     │
│  [🔓 Đăng Nhập]   ← Button          │
│                                     │
│  Chưa có tài khoản? Đăng ký ngay    │
└─────────────────────────────────────┘
```

---

## 🚀 **CÁCH SỬ DỤNG**

### **1. Truy Cập Trang Auth:**

**URL:**
- http://localhost:8000/login
- http://localhost:8000/register

**Hoặc từ trang chính:**
- Click nút "Đăng Nhập" hoặc "Đăng Ký" ở header

### **2. Đăng Ký:**

**Bước 1:** Click tab "Đăng Ký"

**Bước 2:** Điền form:
```
Thông Tin Cơ Bản:
  📧 Email: example@gmail.com
  👤 Họ và Tên: Nguyễn Văn A

Thông Tin Thể Chất:
  🎂 Tuổi: 25
  📏 Chiều cao: 170 cm
  ⚖️ Cân nặng: 70 kg

Thông Tin Tập Luyện:
  💪 Loại Cơ Thể: Mesomorph
  📊 Trình Độ: Intermediate
  🎯 Mục Tiêu: Tăng cơ bắp
  📅 Số Ngày/Tuần: 4 ngày
```

**Bước 3:** Click "✨ Tạo Tài Khoản"

**Bước 4:** Tự động redirect về trang chính

### **3. Đăng Nhập:**

**Bước 1:** Click tab "Đăng Nhập"

**Bước 2:** Nhập email đã đăng ký

**Bước 3:** (Optional) Check "Ghi nhớ đăng nhập"

**Bước 4:** Click "🔓 Đăng Nhập"

**Bước 5:** Tự động redirect về trang chính

---

## 🔧 **API ENDPOINTS**

### **POST /api/users/by-email**

Tìm user theo email (cho login)

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response (Success):**
```json
{
  "success": true,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "Nguyễn Văn A",
    "body_type": "mesomorph",
    "fitness_level": "Intermediate",
    ...
  }
}
```

**Response (Not Found):**
```json
{
  "success": false,
  "user": null,
  "message": "User not found"
}
```

### **POST /api/users**

Tạo user mới (cho register) - Đã có sẵn từ trước

**Request:**
```json
{
  "email": "user@example.com",
  "full_name": "Nguyễn Văn A",
  "age": 25,
  "height": 170,
  "weight": 70,
  "body_type": "mesomorph",
  "fitness_level": "Intermediate",
  "primary_goal": "muscle_gain",
  "days_per_week": 4
}
```

---

## 📊 **LUỒNG HOẠT ĐỘNG**

### **Register Flow:**

```
User vào /register
    ↓
Điền form
    ↓
Submit form
    ↓
auth.js → POST /api/users
    ↓
app.py → supabase.create_user()
    ↓
Supabase → INSERT INTO users
    ↓
Return user với UUID
    ↓
auth.js → Save user_id to localStorage
    ↓
Redirect to /
    ↓
Main app → Check localStorage
    ↓
Show: ✅ Đã đăng nhập
```

### **Login Flow:**

```
User vào /login
    ↓
Nhập email
    ↓
Submit form
    ↓
auth.js → POST /api/users/by-email
    ↓
app.py → supabase.get_user_by_email()
    ↓
Supabase → SELECT FROM users WHERE email = ?
    ↓
Return user (nếu tồn tại)
    ↓
auth.js → Save user_id to localStorage
    ↓
Redirect to /
    ↓
Main app → Check localStorage
    ↓
Show: ✅ Đã đăng nhập
```

---

## 💾 **DATA PERSISTENCE**

### **LocalStorage:**

**Keys:**
```javascript
// User ID
localStorage.setItem('userId', 'uuid');

// Remember Me
localStorage.setItem('rememberMe', 'true');

// Session ID
localStorage.setItem('sessionId', 'uuid');
```

**Check on Page Load:**
```javascript
const userId = localStorage.getItem('userId');
if (userId) {
  // Already logged in
  // Redirect to home or show logged in state
}
```

---

## 🎨 **CUSTOMIZATION**

### **Colors (CSS Variables):**

Sửa trong `static/auth.css`:

```css
:root {
    --primary-color: #667eea;     /* Purple gradient start */
    --secondary-color: #764ba2;   /* Purple gradient end */
    --success-color: #4ecca3;     /* Green for success */
    --error-color: #ff6b6b;       /* Red for errors */
    --warning-color: #ffc93c;     /* Yellow for warnings */
}
```

### **Background Animation:**

Enable/disable trong `static/auth.css`:

```css
/* Tắt animation */
.bg-animation {
    display: none;
}
```

### **Form Fields:**

Thêm/bớt fields trong `static/auth.html`:

```html
<div class="form-group">
    <label for="new-field">
        <span class="icon">🆕</span>
        Field Mới
    </label>
    <input type="text" id="new-field" placeholder="...">
</div>
```

---

## 🔐 **SECURITY**

### **Current Implementation:**

**Email-based Login:**
- ✅ No password (simple for demo)
- ✅ Email uniqueness checked by Supabase
- ⚠️ Not secure for production

**For Production:**

1. **Add Password:**
```javascript
// hash password before sending
const hashedPassword = await bcrypt.hash(password, 10);
```

2. **Add Supabase Auth:**
```javascript
// Use Supabase's built-in authentication
const { data, error } = await supabase.auth.signUp({
  email: email,
  password: password
});
```

3. **Add JWT Tokens:**
```javascript
// Store access token instead of user_id
localStorage.setItem('accessToken', data.session.access_token);
```

4. **Add Session Management:**
```javascript
// Check token expiry
// Refresh token when needed
```

---

## 🐛 **TROUBLESHOOTING**

### **"Email không tồn tại"**

**Nguyên nhân:**
- Email chưa được đăng ký
- Gõ sai email

**Giải pháp:**
- Click "Đăng ký ngay" để tạo tài khoản

### **"Email đã tồn tại"**

**Nguyên nhân:**
- Email đã được đăng ký trước đó

**Giải pháp:**
- Chuyển sang tab "Đăng Nhập"
- Hoặc dùng email khác

### **"Supabase not configured"**

**Nguyên nhân:**
- Chưa setup Supabase
- File `.env` thiếu hoặc sai

**Giải pháp:**
- Setup Supabase theo `QUICK_SUPABASE_SETUP.txt`
- Kiểm tra file `.env`

### **Không redirect sau login**

**Nguyên nhân:**
- JavaScript error
- localStorage bị block

**Giải pháp:**
- F12 → Console → Xem errors
- Check browser settings (allow cookies/storage)

---

## 📱 **RESPONSIVE DESIGN**

### **Mobile Support:**

**Breakpoints:**
```css
/* Tablet */
@media (max-width: 768px) {
  .auth-box {
    padding: 30px 20px;
  }
}

/* Mobile */
@media (max-width: 480px) {
  .auth-box {
    padding: 25px 15px;
  }
}
```

**Features:**
- ✅ Auto adjust form width
- ✅ Stack form rows on mobile
- ✅ Larger touch targets
- ✅ Optimized fonts

---

## 🎯 **NEXT FEATURES (Future)**

### **Planned:**

1. **Password Auth:**
   - Add password field
   - Password strength indicator
   - Forgot password flow

2. **Social Login:**
   - Google Login
   - Facebook Login
   - GitHub Login

3. **Profile Pictures:**
   - Upload avatar
   - Gravatar integration

4. **Email Verification:**
   - Send verification email
   - Verify email on signup

5. **2FA (Two-Factor Auth):**
   - SMS verification
   - Authenticator app

---

## 💡 **TIPS**

### **Development:**

**Auto-fill for testing:**
```javascript
// Add to auth.js for quick testing
document.getElementById('register-email').value = 'test@gym.com';
document.getElementById('register-name').value = 'Test User';
```

**Skip redirect (for debugging):**
```javascript
// Comment out redirect line
// window.location.href = '/';
```

### **Production:**

**Enable HTTPS:**
```python
# Use production server with SSL
uvicorn app:app --host 0.0.0.0 --port 443 --ssl-keyfile key.pem --ssl-certfile cert.pem
```

**Add Rate Limiting:**
```python
# Limit login attempts
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@limiter.limit("5/minute")
@app.post("/api/users/by-email")
async def get_user_by_email(...):
    ...
```

---

## 📊 **FILE STRUCTURE**

```
static/
├── auth.html         # Login/Register page
├── auth.css          # Auth page styling
├── auth.js           # Auth page logic
├── index.html        # Main app (updated with login buttons)
├── script.js         # Main app logic (updated)
└── styles.css        # Main app styling

Backend:
├── app.py            # Added /login, /register, /api/users/by-email
└── supabase_client.py # Already has get_user_by_email()
```

---

## ✅ **CHECKLIST**

**Files Created:**
- ✅ `static/auth.html` (Login/Register page)
- ✅ `static/auth.css` (Styling)
- ✅ `static/auth.js` (Logic)
- ✅ `AUTH_SYSTEM_GUIDE.md` (This file)

**Files Updated:**
- ✅ `app.py` (Added auth endpoints)
- ✅ `static/script.js` (Updated login buttons)

**Features Working:**
- ✅ Login page accessible at /login
- ✅ Register page accessible at /register
- ✅ Login by email
- ✅ Registration with full form
- ✅ Auto redirect after login/register
- ✅ LocalStorage persistence
- ✅ Toast notifications
- ✅ Loading states
- ✅ Responsive design

---

## 🚀 **GET STARTED**

```bash
# 1. Chạy app
python app.py

# 2. Mở browser
http://localhost:8000

# 3. Click "Đăng Ký" ở header

# 4. Hoặc truy cập trực tiếp
http://localhost:8000/register

# 5. Điền form và đăng ký!
```

---

**🎉 Enjoy your new authentication system! 🔐**

*Version: 2.1 - Auth System*  
*Date: October 21, 2025*

