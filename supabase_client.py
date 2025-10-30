"""
Supabase Client for Gym RAG AI Assistant
Module để kết nối và tương tác với Supabase
"""

from supabase import create_client, Client
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseManager:
    """Manager class để quản lý kết nối Supabase"""
    
    def __init__(self):
        """Khởi tạo Supabase client"""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in environment variables")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
    
    # ==================== USERS ====================
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict:
        """Tạo user mới"""
        try:
            response = self.client.table('users').insert(user_data).execute()
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Lấy thông tin user"""
        try:
            response = self.client.table('users').select("*").eq('id', user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Lấy user theo email"""
        try:
            response = self.client.table('users').select("*").eq('email', email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Dict:
        """Cập nhật thông tin user"""
        try:
            response = self.client.table('users').update(updates).eq('id', user_id).execute()
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_last_login(self, user_id: str) -> Dict:
        """Cập nhật thời gian login cuối"""
        return self.update_user(user_id, {"last_login": datetime.now().isoformat()})
    
    # ==================== WORKOUT PLANS ====================
    
    def save_workout_plan(self, user_id: str, plan_data: Dict[str, Any]) -> Dict:
        """Lưu kế hoạch tập luyện"""
        try:
            workout_plan = {
                "user_id": user_id,
                "plan_name": plan_data.get("plan_name", f"Plan {datetime.now().strftime('%Y-%m-%d')}"),
                "description": plan_data.get("description", ""),
                "body_type": plan_data.get("body_type"),
                "fitness_level": plan_data.get("fitness_level"),
                "goals": plan_data.get("goals"),
                "days_per_week": plan_data.get("days_per_week", 3),
                "plan_data": plan_data,
                "is_active": True
            }
            
            response = self.client.table('workout_plans').insert(workout_plan).execute()
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_user_workout_plans(self, user_id: str, active_only: bool = False) -> List[Dict]:
        """Lấy danh sách workout plans của user"""
        try:
            query = self.client.table('workout_plans').select("*").eq('user_id', user_id)
            
            if active_only:
                query = query.eq('is_active', True)
            
            response = query.order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error getting workout plans: {e}")
            return []
    
    def get_workout_plan(self, plan_id: str) -> Optional[Dict]:
        """Lấy chi tiết 1 workout plan"""
        try:
            response = self.client.table('workout_plans').select("*").eq('id', plan_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting workout plan: {e}")
            return None
    
    def update_workout_plan(self, plan_id: str, updates: Dict[str, Any]) -> Dict:
        """Cập nhật workout plan"""
        try:
            response = self.client.table('workout_plans').update(updates).eq('id', plan_id).execute()
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def toggle_plan_favorite(self, plan_id: str, is_favorite: bool) -> Dict:
        """Đánh dấu/bỏ đánh dấu plan yêu thích"""
        return self.update_workout_plan(plan_id, {"is_favorite": is_favorite})
    
    def delete_workout_plan(self, plan_id: str) -> Dict:
        """Xóa workout plan"""
        try:
            self.client.table('workout_plans').delete().eq('id', plan_id).execute()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== FAVORITE EXERCISES ====================
    
    def add_favorite_exercise(self, user_id: str, exercise_data: Dict[str, Any]) -> Dict:
        """Thêm bài tập vào favorites"""
        try:
            favorite = {
                "user_id": user_id,
                "exercise_id": exercise_data.get("id"),
                "exercise_title": exercise_data.get("title"),
                "exercise_data": exercise_data,
                "personal_notes": exercise_data.get("notes", ""),
                "times_performed": 0
            }
            
            response = self.client.table('favorite_exercises').insert(favorite).execute()
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_favorite_exercises(self, user_id: str) -> List[Dict]:
        """Lấy danh sách bài tập yêu thích"""
        try:
            response = self.client.table('favorite_exercises').select("*").eq('user_id', user_id).order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error getting favorites: {e}")
            return []
    
    def remove_favorite_exercise(self, user_id: str, exercise_id: str) -> Dict:
        """Xóa bài tập khỏi favorites"""
        try:
            self.client.table('favorite_exercises').delete().eq('user_id', user_id).eq('exercise_id', exercise_id).execute()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_exercise_performance(self, user_id: str, exercise_id: str) -> Dict:
        """Cập nhật số lần thực hiện bài tập"""
        try:
            # Increment times_performed
            response = self.client.rpc('increment_exercise_performed', {
                'user_id_param': user_id,
                'exercise_id_param': exercise_id
            }).execute()
            
            # Update last_performed
            self.client.table('favorite_exercises')\
                .update({"last_performed": datetime.now().isoformat()})\
                .eq('user_id', user_id)\
                .eq('exercise_id', exercise_id)\
                .execute()
            
            return {"success": True}
        except Exception as e:
            # Fallback if RPC doesn't exist
            return {"success": False, "error": str(e)}
    
    # ==================== CHAT HISTORY ====================
    
    def save_chat(self, user_id: str, session_id: str, user_message: str, 
                  ai_response: str, exercises_suggested: List[Dict] = None, 
                  context_used: str = None) -> Dict:
        """Lưu lịch sử chat"""
        try:
            chat = {
                "user_id": user_id,
                "session_id": session_id,
                "user_message": user_message,
                "ai_response": ai_response,
                "exercises_suggested": exercises_suggested or [],
                "context_used": context_used
            }
            
            response = self.client.table('chat_history').insert(chat).execute()
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_chat_history(self, user_id: str, session_id: str = None, limit: int = 50) -> List[Dict]:
        """Lấy lịch sử chat"""
        try:
            query = self.client.table('chat_history').select("*").eq('user_id', user_id)
            
            if session_id:
                query = query.eq('session_id', session_id)
            
            response = query.order('created_at', desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []
    
    # ==================== PROGRESS TRACKING ====================
    
    def add_progress_entry(self, user_id: str, progress_data: Dict[str, Any]) -> Dict:
        """Thêm entry theo dõi tiến độ"""
        try:
            progress = {
                "user_id": user_id,
                "measurement_date": progress_data.get("date", date.today().isoformat()),
                **progress_data
            }
            
            response = self.client.table('progress_tracking').insert(progress).execute()
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_progress_history(self, user_id: str, limit: int = 30) -> List[Dict]:
        """Lấy lịch sử tiến độ"""
        try:
            response = self.client.table('progress_tracking')\
                .select("*")\
                .eq('user_id', user_id)\
                .order('measurement_date', desc=True)\
                .limit(limit)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting progress: {e}")
            return []
    
    def get_latest_progress(self, user_id: str) -> Optional[Dict]:
        """Lấy entry tiến độ mới nhất"""
        try:
            response = self.client.table('progress_tracking')\
                .select("*")\
                .eq('user_id', user_id)\
                .order('measurement_date', desc=True)\
                .limit(1)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting latest progress: {e}")
            return None
    
    # ==================== WORKOUT SESSIONS ====================
    
    def log_workout_session(self, user_id: str, session_data: Dict[str, Any]) -> Dict:
        """Ghi lại buổi tập thực tế"""
        try:
            session = {
                "user_id": user_id,
                "workout_plan_id": session_data.get("plan_id"),
                "session_date": session_data.get("date", date.today().isoformat()),
                "duration_minutes": session_data.get("duration"),
                "exercises_completed": session_data.get("exercises", []),
                "difficulty_rating": session_data.get("difficulty_rating"),
                "satisfaction_rating": session_data.get("satisfaction_rating"),
                "notes": session_data.get("notes", "")
            }
            
            response = self.client.table('workout_sessions').insert(session).execute()
            
            # Update workout plan times_completed if plan_id exists
            if session_data.get("plan_id"):
                self.client.table('workout_plans')\
                    .update({
                        "times_completed": self.client.table('workout_plans').select('times_completed').eq('id', session_data['plan_id']),
                        "last_completed": datetime.now().isoformat()
                    })\
                    .eq('id', session_data['plan_id'])\
                    .execute()
            
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_workout_sessions(self, user_id: str, limit: int = 30) -> List[Dict]:
        """Lấy lịch sử buổi tập"""
        try:
            response = self.client.table('workout_sessions')\
                .select("*")\
                .eq('user_id', user_id)\
                .order('session_date', desc=True)\
                .limit(limit)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting sessions: {e}")
            return []
    
    # ==================== USER SETTINGS ====================
    
    def get_user_settings(self, user_id: str) -> Optional[Dict]:
        """Lấy settings của user"""
        try:
            response = self.client.table('user_settings').select("*").eq('user_id', user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting settings: {e}")
            return None
    
    def create_user_settings(self, user_id: str, settings: Dict[str, Any] = None) -> Dict:
        """Tạo settings mặc định cho user"""
        try:
            default_settings = {
                "user_id": user_id,
                "preferred_language": "vi",
                "theme": "dark",
                "email_notifications": True,
                "workout_reminders": True,
                "weight_unit": "kg",
                "height_unit": "cm"
            }
            
            if settings:
                default_settings.update(settings)
            
            response = self.client.table('user_settings').insert(default_settings).execute()
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_user_settings(self, user_id: str, updates: Dict[str, Any]) -> Dict:
        """Cập nhật settings"""
        try:
            response = self.client.table('user_settings').update(updates).eq('user_id', user_id).execute()
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== STATISTICS ====================
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Lấy thống kê tổng quan của user"""
        try:
            # Count workout plans
            plans_count = len(self.client.table('workout_plans').select("id", count='exact').eq('user_id', user_id).execute().data)
            
            # Count favorites
            favorites_count = len(self.client.table('favorite_exercises').select("id", count='exact').eq('user_id', user_id).execute().data)
            
            # Count sessions
            sessions_count = len(self.client.table('workout_sessions').select("id", count='exact').eq('user_id', user_id).execute().data)
            
            # Latest progress
            latest_progress = self.get_latest_progress(user_id)
            
            return {
                "total_plans": plans_count,
                "total_favorites": favorites_count,
                "total_sessions": sessions_count,
                "latest_weight": latest_progress.get('weight') if latest_progress else None,
                "latest_measurement_date": latest_progress.get('measurement_date') if latest_progress else None
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}


# Singleton instance
_supabase_manager = None

def get_supabase_manager() -> SupabaseManager:
    """Get singleton instance of SupabaseManager"""
    global _supabase_manager
    if _supabase_manager is None:
        _supabase_manager = SupabaseManager()
    return _supabase_manager


# Example usage
if __name__ == "__main__":
    # Test connection
    try:
        sb = get_supabase_manager()
        print("✅ Connected to Supabase successfully!")
        
        # Example: Create a test user
        # user_data = {
        #     "email": "test@example.com",
        #     "full_name": "Test User",
        #     "body_type": "mesomorph",
        #     "fitness_level": "Intermediate",
        #     "primary_goal": "muscle_gain"
        # }
        # result = sb.create_user(user_data)
        # print(f"User created: {result}")
        
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")

