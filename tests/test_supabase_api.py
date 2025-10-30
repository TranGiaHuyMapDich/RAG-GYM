"""
Script test API với Supabase
Chạy script này để test các endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_user():
    """Test tạo user mới"""
    print("\n=== TEST 1: Tạo User Mới ===")
    
    user_data = {
        "email": "test@gym.com",
        "full_name": "Nguyễn Văn Test",
        "body_type": "mesomorph",
        "fitness_level": "Intermediate",
        "height": 170,
        "weight": 70,
        "age": 25,
        "primary_goal": "muscle_gain",
        "available_equipment": ["Barbell", "Dumbbell"],
        "days_per_week": 4
    }
    
    response = requests.post(f"{BASE_URL}/api/users", json=user_data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Tạo user thành công!")
        print(f"   User ID: {result['user']['id']}")
        print(f"   Email: {result['user']['email']}")
        return result['user']['id']
    else:
        print(f"❌ Lỗi: {response.text}")
        return None


def test_create_workout_plan(user_id):
    """Test tạo workout plan"""
    print("\n=== TEST 2: Tạo Workout Plan ===")
    
    plan_data = {
        "body_type": "mesomorph",
        "fitness_level": "Intermediate",
        "goals": "muscle_gain",
        "days_per_week": 4,
        "height": 170,
        "weight": 70,
        "age": 25,
        "user_id": user_id,
        "plan_name": "4-Day Test Plan"
    }
    
    response = requests.post(f"{BASE_URL}/api/workout-plan", json=plan_data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Tạo workout plan thành công!")
        if 'saved_plan_id' in result:
            print(f"   Plan ID: {result['saved_plan_id']}")
            print(f"   Message: {result.get('message')}")
            return result['saved_plan_id']
        else:
            print("   ⚠️ Plan tạo thành công nhưng không lưu vào Supabase")
            return None
    else:
        print(f"❌ Lỗi: {response.text}")
        return None


def test_chat_with_history(user_id):
    """Test chat và lưu history"""
    print("\n=== TEST 3: Chat với AI (có lưu history) ===")
    
    chat_data = {
        "question": "Bài tập ngực cho người mới bắt đầu",
        "n_results": 3,
        "user_id": user_id
    }
    
    response = requests.post(f"{BASE_URL}/api/chat", json=chat_data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Chat thành công!")
        print(f"   Số bài tập gợi ý: {len(result['exercises'])}")
        print(f"   Bài tập đầu tiên: {result['exercises'][0]['title']}")
    else:
        print(f"❌ Lỗi: {response.text}")


def test_get_user_plans(user_id):
    """Test lấy danh sách workout plans"""
    print("\n=== TEST 4: Lấy Danh Sách Workout Plans ===")
    
    response = requests.get(f"{BASE_URL}/api/users/{user_id}/workout-plans")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Lấy plans thành công!")
        print(f"   Số plans: {len(result['plans'])}")
        for i, plan in enumerate(result['plans'], 1):
            print(f"   {i}. {plan['plan_name']} - {plan['days_per_week']} ngày/tuần")
    else:
        print(f"❌ Lỗi: {response.text}")


def test_add_favorite(user_id):
    """Test thêm bài tập vào favorites"""
    print("\n=== TEST 5: Thêm Bài Tập Yêu Thích ===")
    
    favorite_data = {
        "exercise_id": "123",
        "exercise_title": "Barbell Bench Press",
        "exercise_data": {
            "bodypart": "Chest",
            "equipment": "Barbell",
            "level": "Intermediate",
            "rating": "9.2"
        },
        "notes": "Bài tập tuyệt vời cho ngực"
    }
    
    response = requests.post(f"{BASE_URL}/api/users/{user_id}/favorites", json=favorite_data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Thêm favorite thành công!")
        print(f"   Bài tập: {result['favorite']['exercise_title']}")
    else:
        print(f"❌ Lỗi: {response.text}")


def test_get_favorites(user_id):
    """Test lấy danh sách favorites"""
    print("\n=== TEST 6: Lấy Danh Sách Favorites ===")
    
    response = requests.get(f"{BASE_URL}/api/users/{user_id}/favorites")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Lấy favorites thành công!")
        print(f"   Số favorites: {len(result['favorites'])}")
        for fav in result['favorites']:
            print(f"   - {fav['exercise_title']}")
    else:
        print(f"❌ Lỗi: {response.text}")


def test_add_progress(user_id):
    """Test thêm progress tracking"""
    print("\n=== TEST 7: Thêm Progress Entry ===")
    
    progress_data = {
        "weight": 72.5,
        "body_fat_percentage": 15.2,
        "notes": "Cảm thấy khỏe hơn"
    }
    
    response = requests.post(f"{BASE_URL}/api/users/{user_id}/progress", json=progress_data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Thêm progress thành công!")
        print(f"   Cân nặng: {result['progress']['weight']} kg")
    else:
        print(f"❌ Lỗi: {response.text}")


def test_get_user_stats(user_id):
    """Test lấy stats"""
    print("\n=== TEST 8: Lấy User Statistics ===")
    
    response = requests.get(f"{BASE_URL}/api/users/{user_id}/stats")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Lấy stats thành công!")
        stats = result['stats']
        print(f"   Total Plans: {stats['total_plans']}")
        print(f"   Total Favorites: {stats['total_favorites']}")
        print(f"   Latest Weight: {stats.get('latest_weight')} kg")
    else:
        print(f"❌ Lỗi: {response.text}")


def test_chat_history(user_id):
    """Test lấy chat history"""
    print("\n=== TEST 9: Lấy Chat History ===")
    
    response = requests.get(f"{BASE_URL}/api/users/{user_id}/chat-history?limit=10")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Lấy chat history thành công!")
        print(f"   Số messages: {len(result['history'])}")
        if result['history']:
            print(f"   Message mới nhất: {result['history'][0]['user_message']}")
    else:
        print(f"❌ Lỗi: {response.text}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🏋️ TEST SUPABASE API INTEGRATION")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/statistics")
        if response.status_code != 200:
            print("❌ Server không chạy. Hãy chạy: python app.py")
            return
    except Exception as e:
        print(f"❌ Không thể kết nối server: {e}")
        print("   Hãy chạy: python app.py")
        return
    
    print("✅ Server đang chạy!")
    
    # Run tests
    user_id = test_create_user()
    
    if user_id:
        test_create_workout_plan(user_id)
        test_chat_with_history(user_id)
        test_add_favorite(user_id)
        test_add_progress(user_id)
        
        # Get data
        test_get_user_plans(user_id)
        test_get_favorites(user_id)
        test_chat_history(user_id)
        test_get_user_stats(user_id)
    
    print("\n" + "="*60)
    print("✅ HOÀN THÀNH TẤT CẢ TESTS!")
    print("="*60)
    print(f"\n💡 User ID để test thêm: {user_id}")
    print("\n")


if __name__ == "__main__":
    main()

