"""
FastAPI Web Application for Gym RAG Assistant
Ứng dụng web trợ lý gym thông minh
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
from rag_system_simple import GymRAGSystem
from supabase_client import get_supabase_manager
import os
import uuid
from datetime import datetime
from deep_translator import GoogleTranslator

# Khởi tạo FastAPI app
app = FastAPI(title="Gym RAG Assistant", description="Trợ lý gym thông minh sử dụng RAG AI")

# Khởi tạo RAG system
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("Đang khởi tạo Gym RAG System...")
rag_system = GymRAGSystem("data/megaGymDataset.csv")
rag_system.initialize_vector_store(force_recreate=False)
print("Hệ thống RAG đã sẵn sàng!")

# Khởi tạo Supabase (optional - sẽ skip nếu không có .env)
try:
    supabase = get_supabase_manager()
    print("✅ Kết nối Supabase thành công!")
    SUPABASE_ENABLED = True
except Exception as e:
    print(f"⚠️ Supabase không khả dụng: {e}")
    print("   Ứng dụng sẽ chạy mà không lưu vào database")
    supabase = None
    SUPABASE_ENABLED = False

# Pydantic models cho request/response
class ChatRequest(BaseModel):
    question: str
    n_results: Optional[int] = 5
    user_id: Optional[str] = None  # Optional user_id để lưu chat history
    session_id: Optional[str] = None
    # target language for the response (e.g. 'vi' for Vietnamese). Default to 'vi' to return VN content.
    target: Optional[str] = 'vi'

class WorkoutPlanRequest(BaseModel):
    body_type: str  # ectomorph, mesomorph, endomorph
    fitness_level: str  # Beginner, Intermediate, Advanced
    goals: str  # muscle_gain, weight_loss, endurance, strength, general_fitness
    available_equipment: Optional[List[str]] = None
    days_per_week: Optional[int] = 3
    height: Optional[float] = None  # cm
    weight: Optional[float] = None  # kg
    age: Optional[int] = None
    user_id: Optional[str] = None  # Optional user_id để lưu plan
    plan_name: Optional[str] = None

class ExerciseFilterRequest(BaseModel):
    body_part: Optional[str] = None
    equipment: Optional[str] = None
    level: Optional[str] = None
    limit: Optional[int] = 10

# New models for Supabase integration
class UserCreate(BaseModel):
    email: str
    full_name: Optional[str] = None
    body_type: Optional[str] = None
    fitness_level: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    primary_goal: Optional[str] = None
    available_equipment: Optional[List[str]] = None
    days_per_week: Optional[int] = 3

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    body_type: Optional[str] = None
    fitness_level: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    primary_goal: Optional[str] = None
    available_equipment: Optional[List[str]] = None
    days_per_week: Optional[int] = None

class FavoriteExerciseRequest(BaseModel):
    exercise_id: str
    exercise_title: str
    exercise_data: Optional[Dict] = None
    notes: Optional[str] = None

class ProgressEntry(BaseModel):
    weight: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    notes: Optional[str] = None
    measurement_date: Optional[str] = None

class TranslateRequest(BaseModel):
    text: str
    source: Optional[str] = 'en'
    target: Optional[str] = 'vi'


# Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Trang chủ"""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Endpoint để chat với RAG AI (có lưu vào Supabase nếu có user_id)
    """
    try:
        # Tìm kiếm thông tin liên quan
        results = rag_system.search(request.question, n_results=request.n_results)

        # Nếu không tìm thấy kết quả phù hợp trong dataset (hoặc kết quả không đủ liên quan),
        # trả về thông báo rõ ràng cho người dùng yêu cầu đặt câu hỏi khác.
        relevance_threshold = 0.6  # distance (1-similarity) > 0.6 -> not relevant
        if not results or (len(results) > 0 and results[0].get('distance', 1.0) > relevance_threshold):
            # Fallback message in Vietnamese (as requested)
            fallback_msg = "câu hỏi của bạn không có trong bộ dataset tôi đã học, vui lòng đặt câu hỏi khác"
            # If user requested another language (unlikely), attempt to translate the fallback
            if request.target and request.target != 'vi':
                try:
                    translator = GoogleTranslator(source='auto', target=request.target)
                    fallback_msg = translator.translate(fallback_msg)
                except Exception:
                    pass
            return {"answer": fallback_msg, "exercises": [], "context": ""}

        # Tạo context từ kết quả tìm kiếm
        context_parts = []
        exercises = []

        for i, result in enumerate(results, 1):
            context_parts.append(f"{i}. {result['text']}")
            exercises.append({
                'title': result['metadata'].get('title', ''),
                'bodypart': result['metadata'].get('bodypart', ''),
                'equipment': result['metadata'].get('equipment', ''),
                'level': result['metadata'].get('level', ''),
                'rating': result['metadata'].get('rating', '')
            })

        context = "\n\n".join(context_parts)

        # Tạo response (original text contains dataset content)
        response_text = f"""Dựa trên cơ sở dữ liệu của tôi, tôi tìm thấy {len(results)} bài tập phù hợp với câu hỏi của bạn:\n\n{context}\n\nCác bài tập này được sắp xếp theo độ liên quan với câu hỏi của bạn. Bạn có thể xem chi tiết từng bài tập bên dưới."""

        # Lưu chat history vào Supabase (nếu có user_id và Supabase enabled)
        if SUPABASE_ENABLED and request.user_id:
            try:
                session_id = request.session_id or str(uuid.uuid4())
                supabase.save_chat(
                    user_id=request.user_id,
                    session_id=session_id,
                    user_message=request.question,
                    ai_response=response_text,
                    exercises_suggested=exercises,
                    context_used=context
                )
            except Exception as db_error:
                print(f"⚠️ Không thể lưu chat vào Supabase: {db_error}")

        # If the client requested translation (e.g., 'vi'), translate the response and exercises
        translated_answer = None
        translated_exercises = None
        if request.target and request.target != 'en':
            try:
                translator = GoogleTranslator(source='auto', target=request.target)
                # Translate the whole API answer (this will translate the embedded context too)
                translated_answer = translator.translate(response_text)

                translated_exercises = []
                for ex in exercises:
                    ex_trans = ex.copy()
                    for fld in ['title', 'bodypart', 'equipment', 'level']:
                        try:
                            if ex.get(fld):
                                ex_trans[f"{fld}_translated"] = translator.translate(str(ex[fld]))
                            else:
                                ex_trans[f"{fld}_translated"] = ''
                        except Exception:
                            ex_trans[f"{fld}_translated"] = ex.get(fld, '')
                    translated_exercises.append(ex_trans)
            except Exception:
                translated_answer = None
                translated_exercises = None

        # Return original and translated versions (frontend can prefer translated fields)
        return {
            "answer": response_text,
            "answer_translated": translated_answer,
            "exercises": exercises,
            "exercises_translated": translated_exercises,
            "context": context
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.post("/api/workout-plan")
async def create_workout_plan(request: WorkoutPlanRequest):
    """
    Tạo kế hoạch tập luyện cá nhân hóa
    """
    try:
        # Tính BMI nếu có thông tin
        bmi = None
        bmi_category = None
        if request.height and request.weight:
            height_m = request.height / 100
            bmi = request.weight / (height_m ** 2)
            
            if bmi < 18.5:
                bmi_category = "Thiếu cân"
            elif 18.5 <= bmi < 25:
                bmi_category = "Bình thường"
            elif 25 <= bmi < 30:
                bmi_category = "Thừa cân"
            else:
                bmi_category = "Béo phì"
        
        # Tạo kế hoạch tập luyện
        plan = rag_system.generate_workout_plan(
            body_type=request.body_type,
            fitness_level=request.fitness_level,
            goals=request.goals,
            available_equipment=request.available_equipment,
            days_per_week=request.days_per_week
        )
        
        # Thêm thông tin BMI vào response
        plan['user_info'] = {
            'height': request.height,
            'weight': request.weight,
            'age': request.age,
            'bmi': round(bmi, 2) if bmi else None,
            'bmi_category': bmi_category
        }
        
        # Thêm lời khuyên dựa trên body type và mục tiêu
        recommendations = []
        
        if request.body_type == 'ectomorph':
            recommendations.append("🏋️ Người gầy (Ectomorph): Tập trung vào tập tạ nặng, ít cardio, ăn nhiều protein và carbs.")
            recommendations.append("💪 Tăng cường khối lượng tập luyện với trọng lượng cao, số lần lặp lại thấp (6-8 reps).")
        elif request.body_type == 'mesomorph':
            recommendations.append("💪 Người cơ bắp (Mesomorph): Cân bằng giữa cardio và tập sức mạnh, dễ tăng cơ và giảm mỡ.")
            recommendations.append("🔥 Kết hợp đa dạng các bài tập, số lần lặp lại trung bình (8-12 reps).")
        elif request.body_type == 'endomorph':
            recommendations.append("🏃 Người dễ tăng cân (Endomorph): Kết hợp nhiều cardio, tập sức mạnh với cường độ cao.")
            recommendations.append("🔥 Tập circuit training, HIIT để tăng đốt cháy calo, số lần lặp lại cao (12-15 reps).")
        
        if request.goals == 'muscle_gain':
            recommendations.append("🎯 Mục tiêu tăng cơ: Progressive overload, ăn thặng dư calo, nghỉ ngơi đủ.")
        elif request.goals == 'weight_loss':
            recommendations.append("🎯 Mục tiêu giảm cân: Deficit calo, tăng cardio, giữ protein cao.")
        elif request.goals == 'strength':
            recommendations.append("🎯 Mục tiêu tăng sức mạnh: Tập nặng (3-5 reps), compound exercises, nghỉ dài giữa các set.")
        elif request.goals == 'endurance':
            recommendations.append("🎯 Mục tiêu tăng sức bền: Reps cao, nghỉ ngắn, nhiều cardio.")
        
        if bmi_category:
            if bmi_category == "Thiếu cân":
                recommendations.append(f"⚖️ BMI: {bmi:.1f} ({bmi_category}) - Nên tăng cường dinh dưỡng và tập luyện sức mạnh.")
            elif bmi_category == "Thừa cân" or bmi_category == "Béo phì":
                recommendations.append(f"⚖️ BMI: {bmi:.1f} ({bmi_category}) - Nên kết hợp cardio và kiểm soát calo.")
            else:
                recommendations.append(f"⚖️ BMI: {bmi:.1f} ({bmi_category}) - Chỉ số cơ thể lý tưởng!")
        
        plan['recommendations'] = recommendations
        
        # Lưu workout plan vào Supabase (nếu có user_id và Supabase enabled)
        if SUPABASE_ENABLED and request.user_id:
            try:
                plan_name = request.plan_name or f"Plan {datetime.now().strftime('%d/%m/%Y')}"
                save_result = supabase.save_workout_plan(
                    user_id=request.user_id,
                    plan_data={
                        **plan,
                        "plan_name": plan_name
                    }
                )
                if save_result.get("success"):
                    plan['saved_plan_id'] = save_result['data']['id']
                    plan['message'] = "✅ Kế hoạch đã được lưu vào database"
            except Exception as db_error:
                print(f"⚠️ Không thể lưu workout plan vào Supabase: {db_error}")
                plan['message'] = "⚠️ Không thể lưu vào database"
        
        return plan
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.post("/api/exercises/filter")
async def filter_exercises(request: ExerciseFilterRequest):
    """
    Lọc bài tập theo tiêu chí
    """
    try:
        exercises = rag_system.get_exercise_by_filters(
            body_part=request.body_part,
            equipment=request.equipment,
            level=request.level,
            limit=request.limit
        )
        
        return {
            "total": len(exercises),
            "exercises": exercises
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.get("/api/statistics")
async def get_statistics():
    """
    Lấy thống kê về dataset
    """
    try:
        stats = rag_system.get_statistics()
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.get("/api/body-parts")
async def get_body_parts():
    """Lấy danh sách các nhóm cơ"""
    try:
        stats = rag_system.get_statistics()
        body_parts = list(stats['body_parts'].keys())
        return {"body_parts": body_parts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.get("/api/equipment")
async def get_equipment():
    """Lấy danh sách thiết bị"""
    try:
        stats = rag_system.get_statistics()
        equipment = list(stats['equipment_types'].keys())
        return {"equipment": equipment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


# ==================== SUPABASE ENDPOINTS ====================

@app.post("/api/users")
async def create_user(user: UserCreate):
    """Tạo user mới"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        result = supabase.create_user(user.dict())
        if result.get("success"):
            return {"success": True, "user": result['data']}
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    """Lấy thông tin user"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        user = supabase.get_user(user_id)
        if user:
            return {"success": True, "user": user}
        else:
            raise HTTPException(status_code=404, detail="User không tồn tại")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.put("/api/users/{user_id}")
async def update_user(user_id: str, updates: UserUpdate):
    """Cập nhật thông tin user"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        # Remove None values
        update_data = {k: v for k, v in updates.dict().items() if v is not None}
        result = supabase.update_user(user_id, update_data)
        
        if result.get("success"):
            return {"success": True, "user": result['data']}
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.get("/api/users/{user_id}/workout-plans")
async def get_user_plans(user_id: str):
    """Lấy danh sách workout plans của user"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        plans = supabase.get_user_workout_plans(user_id)
        return {"success": True, "plans": plans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.get("/api/workout-plans/{plan_id}")
async def get_plan_detail(plan_id: str):
    """Lấy chi tiết 1 workout plan"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        plan = supabase.get_workout_plan(plan_id)
        if plan:
            return {"success": True, "plan": plan}
        else:
            raise HTTPException(status_code=404, detail="Plan không tồn tại")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.delete("/api/workout-plans/{plan_id}")
async def delete_plan(plan_id: str):
    """Xóa workout plan"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        result = supabase.delete_workout_plan(plan_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.post("/api/users/{user_id}/favorites")
async def add_favorite(user_id: str, exercise: FavoriteExerciseRequest):
    """Thêm bài tập vào favorites"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        result = supabase.add_favorite_exercise(user_id, exercise.dict())
        if result.get("success"):
            return {"success": True, "favorite": result['data']}
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.get("/api/users/{user_id}/favorites")
async def get_favorites(user_id: str):
    """Lấy danh sách bài tập yêu thích"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        favorites = supabase.get_favorite_exercises(user_id)
        return {"success": True, "favorites": favorites}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.delete("/api/users/{user_id}/favorites/{exercise_id}")
async def remove_favorite(user_id: str, exercise_id: str):
    """Xóa bài tập khỏi favorites"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        result = supabase.remove_favorite_exercise(user_id, exercise_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.get("/api/users/{user_id}/chat-history")
async def get_chat_history(user_id: str, session_id: Optional[str] = None, limit: int = 50):
    """Lấy lịch sử chat"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        history = supabase.get_chat_history(user_id, session_id, limit)
        return {"success": True, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.post("/api/users/{user_id}/progress")
async def add_progress(user_id: str, progress: ProgressEntry):
    """Thêm entry theo dõi tiến độ"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        result = supabase.add_progress_entry(user_id, progress.dict())
        if result.get("success"):
            return {"success": True, "progress": result['data']}
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.get("/api/users/{user_id}/progress")
async def get_progress(user_id: str, limit: int = 30):
    """Lấy lịch sử tiến độ"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        progress = supabase.get_progress_history(user_id, limit)
        return {"success": True, "progress": progress}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


@app.get("/api/users/{user_id}/stats")
async def get_user_statistics(user_id: str):
    """Lấy thống kê tổng quan của user"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase chưa được cấu hình")
    
    try:
        stats = supabase.get_user_stats(user_id)
        return {"success": True, "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


# Mount static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve auth page
@app.get("/login", response_class=HTMLResponse)
@app.get("/register", response_class=HTMLResponse)
async def auth_page():
    """Serve login/register page"""
    try:
        with open("static/auth.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Auth page not found</h1>", status_code=404)

# Login endpoint - find user by email
@app.post("/api/users/by-email")
async def get_user_by_email(request: dict):
    """Find user by email for login"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase not configured")
    
    email = request.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    try:
        user = supabase.get_user_by_email(email)
        if user:
            return {"success": True, "user": user}
        else:
            return {"success": False, "user": None, "message": "User not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/translate")
async def translate_text(request: TranslateRequest):
    """
    Dịch text từ English sang Vietnamese (hoặc ngược lại)
    """
    try:
        # Khởi tạo translator
        translator = GoogleTranslator(source=request.source, target=request.target)
        
        # Dịch text
        translated = translator.translate(request.text)
        
        return {
            "success": True,
            "original": request.text,
            "translated": translated,
            "source": request.source,
            "target": request.target
        }
    except Exception as e:
        print(f"Translation error: {e}")
        # Fallback: trả về text gốc nếu dịch thất bại
        return {
            "success": False,
            "original": request.text,
            "translated": request.text,
            "error": str(e)
        }


@app.post("/api/translate-exercise")
async def translate_exercise(exercise: Dict):
    """
    Dịch thông tin bài tập từ English sang Vietnamese
    """
    try:
        translator = GoogleTranslator(source='en', target='vi')
        
        translated_exercise = exercise.copy()
        
        # Dịch các trường quan trọng
        if 'title' in exercise and exercise['title']:
            translated_exercise['title_vi'] = translator.translate(exercise['title'])
        
        if 'bodypart' in exercise and exercise['bodypart']:
            translated_exercise['bodypart_vi'] = translator.translate(exercise['bodypart'])
        
        if 'equipment' in exercise and exercise['equipment']:
            translated_exercise['equipment_vi'] = translator.translate(exercise['equipment'])
        
        if 'level' in exercise and exercise['level']:
            translated_exercise['level_vi'] = translator.translate(exercise['level'])
        
        if 'type' in exercise and exercise['type']:
            translated_exercise['type_vi'] = translator.translate(exercise['type'])
        
        # Giữ nguyên các trường khác
        translated_exercise['original'] = exercise
        
        return {
            "success": True,
            "exercise": translated_exercise
        }
    except Exception as e:
        print(f"Translation error: {e}")
        return {
            "success": False,
            "exercise": exercise,
            "error": str(e)
        }


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🏋️ GYM RAG AI ASSISTANT - TRỢ LÝ GYM THÔNG MINH")
    print("="*60)
    print("\n📝 Khởi động server...")
    print("🌐 Truy cập: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

