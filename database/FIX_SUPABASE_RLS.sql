-- ╔════════════════════════════════════════════════════════════════╗
-- ║           SỬA LỖI SUPABASE RLS - CHẠY SQL NÀY                  ║
-- ╚════════════════════════════════════════════════════════════════╝

-- CÁCH 1: Tắt RLS hoàn toàn (ĐƠN GIẢN NHẤT cho development)
-- Copy và chạy 7 dòng sau:

ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE workout_plans DISABLE ROW LEVEL SECURITY;
ALTER TABLE favorite_exercises DISABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history DISABLE ROW LEVEL SECURITY;
ALTER TABLE progress_tracking DISABLE ROW LEVEL SECURITY;
ALTER TABLE workout_sessions DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_settings DISABLE ROW LEVEL SECURITY;

-- ✅ XONG! Giờ có thể đăng ký được!

-- ═══════════════════════════════════════════════════════════════════

-- HOẶC CÁCH 2: Giữ RLS nhưng sửa policies (PHỨC TẠP HƠN)
-- Chỉ chạy nếu muốn giữ RLS và sửa policies

/*
-- Xóa policies cũ
DROP POLICY IF EXISTS "Users can view own data" ON users;
DROP POLICY IF EXISTS "Users can update own data" ON users;
DROP POLICY IF EXISTS "Users can insert own data" ON users;

-- Tạo policies mới cho phép mọi thao tác (không bảo mật, chỉ cho dev)
CREATE POLICY "Allow all for users" ON users FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for workout_plans" ON workout_plans FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for favorite_exercises" ON favorite_exercises FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for chat_history" ON chat_history FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for progress_tracking" ON progress_tracking FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for workout_sessions" ON workout_sessions FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for user_settings" ON user_settings FOR ALL USING (true) WITH CHECK (true);
*/

-- ═══════════════════════════════════════════════════════════════════
-- LƯU Ý:
-- - Cách 1 (TẮT RLS): Đơn giản, nhanh, OK cho development/testing
-- - Cách 2 (SỬA POLICIES): Phức tạp hơn, dùng khi cần bảo mật
-- 
-- KHUYẾN NGHỊ: Dùng Cách 1 để test app trước, sau này có thể bật lại
-- ═══════════════════════════════════════════════════════════════════

