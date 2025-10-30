# BÁO CÁO TESTCASE - RAG GYM AI GYM ASSISTANT

**Dự án:** RAG GYM - AI Gym Assistant  
**Công nghệ:** Python, FastAPI, RAG AI, Supabase  
**Phiên bản:** 2.1  
**Ngày test:** 22/10/2025  
**Người test:** QA Team

---

## BẢNG TESTCASE TỔNG HỢP

| TC ID | Chức năng | Mô tả Test | Bước thực hiện | Kết quả mong đợi | Kết quả thực tế | Trạng thái | Ghi chú |
|-------|-----------|------------|----------------|------------------|-----------------|------------|---------|
| **TC001** | Đăng ký | Đăng ký với email + tên hợp lệ | 1. Vào /register<br>2. Nhập email mới<br>3. Nhập họ tên<br>4. Click "Đăng Ký" | Tạo user thành công, chuyển sang tab login, email được điền sẵn | Đúng như mong đợi, data lưu vào Supabase | ✅ PASS | - |
| **TC002** | Đăng ký | Đăng ký với email trùng | 1. Nhập email đã tồn tại<br>2. Click "Đăng Ký" | Hiện lỗi "Email đã tồn tại" | Hiện lỗi "Email đã tồn tại" | ✅ PASS | - |
| **TC003** | Đăng ký | Đăng ký thiếu thông tin | 1. Để trống email hoặc tên<br>2. Click "Đăng Ký" | Browser validation: "Please fill out this field" | Đúng như mong đợi | ✅ PASS | - |
| **TC004** | Đăng ký | Đăng ký với email sai format | 1. Nhập "test" (không có @)<br>2. Click "Đăng Ký" | Browser validation lỗi format email | Đúng như mong đợi | ✅ PASS | - |
| **TC005** | Đăng nhập | Đăng nhập với email đã đăng ký | 1. Vào /login<br>2. Nhập email đã có<br>3. Click "Đăng Nhập" | Đăng nhập thành công, chuyển về trang chủ, hiện tên user | Đúng như mong đợi, localStorage lưu userId | ✅ PASS | - |
| **TC006** | Đăng nhập | Đăng nhập với email chưa tồn tại | 1. Nhập email chưa đăng ký<br>2. Click "Đăng Nhập" | Hiện lỗi "Email không tồn tại!" | Đúng như mong đợi | ✅ PASS | - |
| **TC007** | Đăng nhập | Đăng nhập với email rỗng | 1. Để trống email<br>2. Click "Đăng Nhập" | Browser validation | Đúng như mong đợi | ✅ PASS | - |
| **TC008** | Đăng xuất | Đăng xuất khi đã login | 1. Click "🚪 Đăng xuất"<br>2. Confirm "OK" | Hiện confirm, đăng xuất, reload trang, localStorage cleared | Đúng như mong đợi | ✅ PASS | - |
| **TC009** | Đăng xuất | Hủy đăng xuất | 1. Click "🚪 Đăng xuất"<br>2. Confirm "Cancel" | Không đăng xuất, vẫn giữ session | Đúng như mong đợi | ✅ PASS | - |
| **TC010** | Chat AI | Chat câu hỏi bài tập | 1. Nhập "chest exercises"<br>2. Click "Gửi" | Hiện loading, AI trả lời với exercise cards, có nút dịch | Đúng như mong đợi, tìm được 15+ exercises | ✅ PASS | - |
| **TC011** | Chat AI | Chat với input rỗng | 1. Để trống<br>2. Click "Gửi" | Không gửi hoặc hiện warning | Không gửi được | ✅ PASS | - |
| **TC012** | Chat AI | Chat khi đã login → auto save | 1. Đăng nhập<br>2. Chat "bicep exercises"<br>3. Kiểm tra Supabase | Chat history lưu vào table `chat_history` với user_id | Data lưu đúng vào Supabase | ✅ PASS | - |
| **TC013** | Chat AI | Chat khi chưa login | 1. Chưa login<br>2. Chat bất kỳ | Chat vẫn hoạt động nhưng không lưu vào DB | Chat hoạt động, không lưu DB | ✅ PASS | Warning hiện "Chưa đăng nhập" |
| **TC014** | Workout Plan | Tạo plan với đầy đủ params | 1. Chọn Level: Intermediate<br>2. Goals: Muscle Gain<br>3. Days: 4<br>4. Click "Tạo Kế Hoạch" | AI tạo workout plan chi tiết theo yêu cầu | Plan được tạo với 4 ngày tập | ✅ PASS | - |
| **TC015** | Workout Plan | Tạo plan khi đã login → auto save | 1. Đăng nhập<br>2. Tạo workout plan<br>3. Check Supabase | Plan lưu vào `workout_plans` table | Data lưu thành công | ✅ PASS | - |
| **TC016** | Workout Plan | Tạo plan thiếu params | 1. Không chọn Level<br>2. Click "Tạo Kế Hoạch" | Browser validation hoặc error | Validation hoạt động | ✅ PASS | - |
| **TC017** | Dịch bài tập | Dịch exercise sang tiếng Việt | 1. Chat để có exercise cards<br>2. Click "🌐 Dịch sang tiếng Việt" | Loading → Nội dung dịch sang tiếng Việt, nút đổi thành "🔄 Hiện bản gốc" | Dịch thành công, UI cập nhật | ✅ PASS | Dùng Google Translate API |
| **TC018** | Dịch bài tập | Chuyển về bản gốc | 1. Sau khi dịch<br>2. Click "🔄 Hiện bản gốc" | Nội dung trở về tiếng Anh | Đúng như mong đợi | ✅ PASS | - |
| **TC019** | Dịch bài tập | Dịch nhiều exercises cùng lúc | 1. Có 5 exercise cards<br>2. Click dịch trên 3 cards | Chỉ card được click mới dịch, các card khác giữ nguyên | Đúng như mong đợi | ✅ PASS | - |
| **TC020** | Supabase | Kết nối Supabase với .env đúng | 1. Có SUPABASE_URL và KEY<br>2. Start app<br>3. Xem logs | Log: "✅ Kết nối Supabase thành công!" | Kết nối OK | ✅ PASS | - |
| **TC021** | Supabase | Kết nối khi thiếu .env | 1. Xóa file .env<br>2. Start app | App vẫn chạy nhưng Supabase disabled, log warning | App chạy, Supabase disabled | ✅ PASS | Fallback mode |
| **TC022** | Supabase | Lưu user vào DB | 1. Đăng ký user mới<br>2. Check Supabase Dashboard | Row mới trong table `users` với đầy đủ fields | Data lưu đúng | ✅ PASS | - |
| **TC023** | Supabase | RLS policy block insert | 1. Enable RLS<br>2. Đăng ký user | Error: "violates row-level security policy" | Lỗi RLS | ❌ FAIL | Cần disable RLS hoặc config policies |
| **TC024** | UI/UX | Responsive trên mobile | 1. Mở DevTools<br>2. Chuyển sang mobile view<br>3. Test các features | Giao diện responsive, không bị vỡ layout | Layout tốt trên iPhone 12 Pro | ✅ PASS | - |
| **TC025** | UI/UX | Responsive trên tablet | 1. Resize browser sang 768px<br>2. Test UI | UI điều chỉnh phù hợp | Đúng như mong đợi | ✅ PASS | - |
| **TC026** | UI/UX | Toast notification hiển thị | 1. Thực hiện actions: đăng ký, login, logout<br>2. Xem notifications | Toast xuất hiện với icon, tự động biến mất sau 3s, có animation | Đúng như mong đợi | ✅ PASS | - |
| **TC027** | UI/UX | Loading spinner | 1. Chat hoặc tạo workout plan<br>2. Xem loading state | Hiện spinner, nút disabled khi loading | Đúng như mong đợi | ✅ PASS | - |
| **TC028** | UI/UX | Dark theme | Mở app | Dark theme áp dụng toàn bộ UI | Đúng như thiết kế | ✅ PASS | - |
| **TC029** | Performance | Load trang chủ | Mở http://localhost:8000 | Trang load < 2s | Load trong ~1.5s | ✅ PASS | - |
| **TC030** | Performance | AI response time | Chat "leg exercises" | Response < 5s | Response ~3-4s | ✅ PASS | Phụ thuộc vector search |
| **TC031** | Performance | Supabase query time | Lấy user data | Query < 1s | Query ~300ms | ✅ PASS | - |
| **TC032** | Security | XSS trong chat input | Nhập `<script>alert('xss')</script>` | Input được escape, không chạy script | Script không chạy | ✅ PASS | - |
| **TC033** | Security | SQL injection | Nhập `test@test.com'; DROP TABLE users; --` | Input được sanitize | Không ảnh hưởng DB | ✅ PASS | Supabase parameterized queries |
| **TC034** | API | GET /api/users/{user_id} với ID hợp lệ | Call API với UUID đúng | Return 200 + user data | Đúng như mong đợi | ✅ PASS | - |
| **TC035** | API | GET /api/users/{user_id} với ID không tồn tại | Call API với UUID fake | Return 404 hoặc null | Return null | ⚠️ WARNING | Nên return 404 thay vì null |
| **TC036** | API | POST /api/users với data hợp lệ | POST email + full_name | Return 200 + user object với ID | Tạo user thành công | ✅ PASS | - |
| **TC037** | API | POST /api/users với email trùng | POST email đã tồn tại | Return 400 + error message | Return error đúng | ✅ PASS | - |
| **TC038** | API | POST /api/chat với message rỗng | POST message="" | Return 400 hoặc validation error | App vẫn process (không validate) | ❌ FAIL | Cần thêm backend validation |
| **TC039** | API | POST /api/translate với text dài (5000 chars) | POST long text | Translate thành công hoặc error rõ ràng | Timeout sau 30s | ❌ FAIL | Cần set timeout hợp lý |
| **TC040** | API | GET /api/users/{user_id}/workout-plans | Call với user có 3 plans | Return array 3 plans | Đúng như mong đợi | ✅ PASS | - |
| **TC041** | Browser | Test trên Chrome | Mở app trên Chrome latest | Tất cả features hoạt động | OK | ✅ PASS | Chrome 120 |
| **TC042** | Browser | Test trên Firefox | Mở app trên Firefox latest | Tất cả features hoạt động | OK | ✅ PASS | Firefox 121 |
| **TC043** | Browser | Test trên Safari | Mở app trên Safari | Tất cả features hoạt động | Một số CSS không đúng | ⚠️ WARNING | Safari 17, minor issues |
| **TC044** | Browser | Test trên Edge | Mở app trên Edge latest | Tất cả features hoạt động | OK | ✅ PASS | Edge 120 |
| **TC045** | Error Handling | Network error khi call API | Ngắt mạng → Chat | Hiện error message rõ ràng | Toast "❌ Lỗi kết nối" | ✅ PASS | - |
| **TC046** | Error Handling | Supabase down | Stop Supabase → Đăng ký | Error message user-friendly | Error 500 với stack trace | ❌ FAIL | Cần catch error tốt hơn |
| **TC047** | Data Persistence | Reload trang sau khi login | 1. Login<br>2. F5 reload | User vẫn login (localStorage) | User vẫn login | ✅ PASS | - |
| **TC048** | Data Persistence | Đóng tab → Mở lại | 1. Login<br>2. Đóng tab<br>3. Mở lại | User vẫn login nếu localStorage còn | User vẫn login | ✅ PASS | - |
| **TC049** | Data Persistence | Clear browser cache | 1. Login<br>2. Clear cache<br>3. Reload | User bị logout | User bị logout | ✅ PASS | - |
| **TC050** | Edge Cases | Chat với 1000 characters | Nhập text rất dài | AI vẫn xử lý được hoặc báo lỗi rõ | AI xử lý OK | ✅ PASS | - |

---

## TỔNG KẾT

### Thống kê

| Metric | Số lượng | Tỷ lệ |
|--------|----------|-------|
| **Tổng testcases** | 50 | 100% |
| **✅ PASS** | 44 | 88% |
| **❌ FAIL** | 4 | 8% |
| **⚠️ WARNING** | 2 | 4% |

### Phân loại theo chức năng

| Chức năng | Tổng | Pass | Fail | Warning |
|-----------|------|------|------|---------|
| Đăng ký/Đăng nhập/Đăng xuất | 9 | 9 | 0 | 0 |
| Chat AI | 4 | 4 | 0 | 0 |
| Workout Plan | 3 | 3 | 0 | 0 |
| Dịch bài tập | 3 | 3 | 0 | 0 |
| Supabase | 4 | 3 | 1 | 0 |
| UI/UX | 5 | 5 | 0 | 0 |
| Performance | 3 | 3 | 0 | 0 |
| Security | 2 | 2 | 0 | 0 |
| API | 7 | 5 | 2 | 1 |
| Browser | 4 | 3 | 0 | 1 |
| Error Handling | 2 | 1 | 1 | 0 |
| Data Persistence | 3 | 3 | 0 | 0 |
| Edge Cases | 1 | 1 | 0 | 0 |

---

## CÁC VẤN ĐỀ CẦN FIX

### ❌ FAIL (4 testcases)

| TC ID | Vấn đề | Mức độ | Giải pháp đề xuất |
|-------|--------|--------|-------------------|
| **TC023** | RLS policy block user registration | 🔴 HIGH | Disable RLS hoặc config policies cho phép insert |
| **TC038** | Không validate message rỗng ở backend | 🟡 MEDIUM | Thêm validation trong FastAPI endpoint |
| **TC039** | Timeout khi dịch text dài (5000 chars) | 🟡 MEDIUM | Set timeout 10s, limit text length 2000 chars |
| **TC046** | Error 500 khi Supabase down | 🟡 MEDIUM | Thêm try-catch, return user-friendly error |

### ⚠️ WARNING (2 testcases)

| TC ID | Vấn đề | Giải pháp đề xuất |
|-------|--------|-------------------|
| **TC035** | API return null thay vì 404 | Return proper HTTP 404 status code |
| **TC043** | Safari CSS không tương thích hoàn toàn | Test và fix CSS cho Safari 17 |

---

## KẾT LUẬN

**Tỷ lệ PASS: 88% (44/50 testcases)**

### Đánh giá tổng quan
- ✅ **Core features** hoạt động ổn định (Đăng ký, Login, Chat AI, Workout Plan, Dịch)
- ✅ **UI/UX** responsive và user-friendly
- ✅ **Performance** đạt yêu cầu
- ✅ **Security** cơ bản OK (XSS, SQL injection)
- ⚠️ **API validation** cần cải thiện
- ⚠️ **Error handling** cần tốt hơn

### Khuyến nghị
1. **Ưu tiên cao:** Fix TC023 (RLS policy) - blocking feature
2. **Trung bình:** Fix TC038, TC039, TC046 - improve robustness
3. **Thấp:** Fix TC035, TC043 - nice to have

### Trạng thái dự án
**✅ SẴN SÀNG CHO DEMO/TESTING**  
**⚠️ CẦN FIX MỘT SỐ LỖI TRƯỚC KHI DEPLOY PRODUCTION**

---

**Ngày báo cáo:** 22/10/2025  
**Version:** 2.1  
**Tester:** QA Team
