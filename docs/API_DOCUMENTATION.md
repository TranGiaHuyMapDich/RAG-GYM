# 📡 API Documentation - Gym RAG AI Assistant

## Base URL
```
http://localhost:8000
```

## Interactive API Docs
FastAPI tự động tạo interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔗 Endpoints

### 1. Get Home Page
```http
GET /
```

**Response**: HTML page (Web interface)

---

### 2. Chat with AI
```http
POST /api/chat
```

**Description**: Hỏi đáp với AI về gym, bài tập, kỹ thuật

**Request Body**:
```json
{
  "question": "string",
  "n_results": 5  // optional, default: 5
}
```

**Example Request**:
```json
{
  "question": "Bài tập ngực cho người mới bắt đầu",
  "n_results": 5
}
```

**Example Response**:
```json
{
  "answer": "Dựa trên cơ sở dữ liệu của tôi, tôi tìm thấy 5 bài tập phù hợp...",
  "exercises": [
    {
      "title": "Barbell Bench Press",
      "bodypart": "Chest",
      "equipment": "Barbell",
      "level": "Beginner",
      "rating": "9.2"
    }
  ],
  "context": "1. Tên bài tập: Barbell Bench Press..."
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"question":"Bài tập ngực cho người mới","n_results":5}'
```

**Python Example**:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "question": "Bài tập ngực cho người mới",
        "n_results": 5
    }
)
print(response.json())
```

**JavaScript Example**:
```javascript
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'Bài tập ngực cho người mới',
    n_results: 5
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

### 3. Generate Workout Plan
```http
POST /api/workout-plan
```

**Description**: Tạo kế hoạch tập luyện cá nhân hóa

**Request Body**:
```json
{
  "body_type": "string",           // required: ectomorph/mesomorph/endomorph
  "fitness_level": "string",       // required: Beginner/Intermediate/Advanced
  "goals": "string",               // required: muscle_gain/weight_loss/strength/endurance/general_fitness
  "available_equipment": ["string"], // optional: list of equipment
  "days_per_week": 3,              // optional: 3-6, default: 3
  "height": 170,                   // optional: in cm
  "weight": 70,                    // optional: in kg
  "age": 25                        // optional
}
```

**Example Request**:
```json
{
  "body_type": "mesomorph",
  "fitness_level": "Intermediate",
  "goals": "muscle_gain",
  "available_equipment": ["Barbell", "Dumbbell"],
  "days_per_week": 4,
  "height": 170,
  "weight": 70,
  "age": 25
}
```

**Example Response**:
```json
{
  "body_type": "mesomorph",
  "fitness_level": "Intermediate",
  "goals": "muscle_gain",
  "days_per_week": 4,
  "recommendations": "Người cơ bắp (Mesomorph): Cân bằng giữa cardio...",
  "user_info": {
    "height": 170,
    "weight": 70,
    "age": 25,
    "bmi": 24.22,
    "bmi_category": "Bình thường"
  },
  "weekly_plan": [
    {
      "day": 1,
      "focus": "Chest, Shoulders, Triceps",
      "exercises": [
        {
          "text": "Tên bài tập: Barbell Bench Press...",
          "metadata": {
            "id": "123",
            "title": "Barbell Bench Press",
            "bodypart": "Chest",
            "equipment": "Barbell",
            "level": "Intermediate",
            "rating": "9.2"
          }
        }
      ]
    }
  ]
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/workout-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "body_type": "mesomorph",
    "fitness_level": "Intermediate",
    "goals": "muscle_gain",
    "days_per_week": 4,
    "height": 170,
    "weight": 70
  }'
```

**Python Example**:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/workout-plan",
    json={
        "body_type": "mesomorph",
        "fitness_level": "Intermediate",
        "goals": "muscle_gain",
        "available_equipment": ["Barbell", "Dumbbell"],
        "days_per_week": 4,
        "height": 170,
        "weight": 70,
        "age": 25
    }
)
plan = response.json()
print(f"Kế hoạch {plan['days_per_week']} ngày/tuần")
for day in plan['weekly_plan']:
    print(f"Ngày {day['day']}: {day['focus']}")
```

---

### 4. Filter Exercises
```http
POST /api/exercises/filter
```

**Description**: Lọc bài tập theo tiêu chí

**Request Body**:
```json
{
  "body_part": "string",    // optional
  "equipment": "string",    // optional
  "level": "string",        // optional: Beginner/Intermediate/Advanced
  "limit": 10               // optional, default: 10
}
```

**Example Request**:
```json
{
  "body_part": "Chest",
  "equipment": "Barbell",
  "level": "Intermediate",
  "limit": 10
}
```

**Example Response**:
```json
{
  "total": 10,
  "exercises": [
    {
      "id": "123",
      "title": "Barbell Bench Press",
      "description": "The barbell bench press is a compound exercise...",
      "type": "Strength",
      "bodypart": "Chest",
      "equipment": "Barbell",
      "level": "Intermediate",
      "rating": "9.2"
    }
  ]
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/exercises/filter" \
  -H "Content-Type: application/json" \
  -d '{
    "body_part": "Chest",
    "equipment": "Barbell",
    "level": "Intermediate",
    "limit": 10
  }'
```

**Python Example**:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/exercises/filter",
    json={
        "body_part": "Chest",
        "equipment": "Barbell",
        "level": "Intermediate",
        "limit": 10
    }
)
data = response.json()
print(f"Tìm thấy {data['total']} bài tập")
for ex in data['exercises']:
    print(f"- {ex['title']} ({ex['rating']}⭐)")
```

---

### 5. Get Statistics
```http
GET /api/statistics
```

**Description**: Lấy thống kê về dataset

**Response**:
```json
{
  "total_exercises": 2920,
  "body_parts": {
    "Chest": 342,
    "Back": 289,
    "Shoulders": 256,
    ...
  },
  "equipment_types": {
    "Barbell": 567,
    "Dumbbell": 498,
    "Machine": 389,
    ...
  },
  "levels": {
    "Beginner": 876,
    "Intermediate": 1234,
    "Advanced": 810
  },
  "types": {
    "Strength": 2456,
    "Cardio": 234,
    "Stretching": 230
  }
}
```

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/statistics"
```

**Python Example**:
```python
import requests

response = requests.get("http://localhost:8000/api/statistics")
stats = response.json()
print(f"Tổng số bài tập: {stats['total_exercises']}")
print(f"Số nhóm cơ: {len(stats['body_parts'])}")
```

---

### 6. Get Body Parts List
```http
GET /api/body-parts
```

**Description**: Lấy danh sách các nhóm cơ

**Response**:
```json
{
  "body_parts": [
    "Abdominals",
    "Biceps",
    "Calves",
    "Chest",
    "Forearms",
    "Glutes",
    "Hamstrings",
    "Lats",
    "Lower Back",
    "Middle Back",
    "Quadriceps",
    "Shoulders",
    "Triceps",
    "Traps"
  ]
}
```

---

### 7. Get Equipment List
```http
GET /api/equipment
```

**Description**: Lấy danh sách thiết bị

**Response**:
```json
{
  "equipment": [
    "Barbell",
    "Dumbbell",
    "Machine",
    "Body Only",
    "Kettlebells",
    "Cable",
    "Bands",
    "Exercise Ball",
    "E-Z Curl Bar",
    "Foam Roll"
  ]
}
```

---

## 📊 Response Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 400  | Bad Request (Invalid input) |
| 422  | Validation Error |
| 500  | Internal Server Error |

---

## 🔒 Error Handling

All endpoints return errors in this format:

```json
{
  "detail": "Error message here"
}
```

Example error response:
```json
{
  "detail": "Lỗi: Dataset not found"
}
```

---

## 📝 Request/Response Models

### ChatRequest
```python
{
  "question": str,           # required
  "n_results": int = 5       # optional
}
```

### WorkoutPlanRequest
```python
{
  "body_type": str,                    # required
  "fitness_level": str,                # required
  "goals": str,                        # required
  "available_equipment": List[str],    # optional
  "days_per_week": int = 3,            # optional
  "height": float,                     # optional
  "weight": float,                     # optional
  "age": int                           # optional
}
```

### ExerciseFilterRequest
```python
{
  "body_part": str,          # optional
  "equipment": str,          # optional
  "level": str,              # optional
  "limit": int = 10          # optional
}
```

---

## 🎯 Use Case Examples

### Example 1: Build a Workout App
```python
import requests

class GymAssistant:
    def __init__(self):
        self.base_url = "http://localhost:8000"
    
    def ask_question(self, question):
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={"question": question, "n_results": 5}
        )
        return response.json()
    
    def create_plan(self, user_profile):
        response = requests.post(
            f"{self.base_url}/api/workout-plan",
            json=user_profile
        )
        return response.json()
    
    def search_exercises(self, filters):
        response = requests.post(
            f"{self.base_url}/api/exercises/filter",
            json=filters
        )
        return response.json()

# Usage
assistant = GymAssistant()

# Ask AI
result = assistant.ask_question("Bài tập ngực tốt nhất")
print(result['answer'])

# Create workout plan
plan = assistant.create_plan({
    "body_type": "mesomorph",
    "fitness_level": "Intermediate",
    "goals": "muscle_gain",
    "days_per_week": 4
})
print(f"Plan created: {plan['days_per_week']} days/week")

# Search exercises
exercises = assistant.search_exercises({
    "body_part": "Chest",
    "level": "Intermediate"
})
print(f"Found {exercises['total']} exercises")
```

### Example 2: CLI Tool
```python
import requests
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py 'your question'")
        return
    
    question = " ".join(sys.argv[1:])
    
    response = requests.post(
        "http://localhost:8000/api/chat",
        json={"question": question}
    )
    
    data = response.json()
    print(f"\n{data['answer']}\n")
    
    print("\nTop Exercises:")
    for i, ex in enumerate(data['exercises'], 1):
        print(f"{i}. {ex['title']}")
        print(f"   Level: {ex['level']} | Equipment: {ex['equipment']}")
        print()

if __name__ == "__main__":
    main()
```

Usage:
```bash
python cli.py "Bài tập ngực cho người mới"
```

### Example 3: Web Integration (JavaScript)
```javascript
class GymAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    async chat(question, nResults = 5) {
        const response = await fetch(`${this.baseURL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question, n_results: nResults })
        });
        return await response.json();
    }

    async createWorkoutPlan(userProfile) {
        const response = await fetch(`${this.baseURL}/api/workout-plan`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userProfile)
        });
        return await response.json();
    }

    async searchExercises(filters) {
        const response = await fetch(`${this.baseURL}/api/exercises/filter`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filters)
        });
        return await response.json();
    }

    async getStatistics() {
        const response = await fetch(`${this.baseURL}/api/statistics`);
        return await response.json();
    }
}

// Usage
const api = new GymAPI();

// Chat
const chatResult = await api.chat('Bài tập ngực cho người mới');
console.log(chatResult.answer);

// Create plan
const plan = await api.createWorkoutPlan({
    body_type: 'mesomorph',
    fitness_level: 'Intermediate',
    goals: 'muscle_gain',
    days_per_week: 4
});
console.log(`Plan: ${plan.days_per_week} days/week`);
```

---

## 🧪 Testing

### Using Python requests
```python
import requests

# Test all endpoints
def test_endpoints():
    base = "http://localhost:8000"
    
    # Test chat
    chat = requests.post(f"{base}/api/chat", 
        json={"question": "test"})
    assert chat.status_code == 200
    
    # Test workout plan
    plan = requests.post(f"{base}/api/workout-plan",
        json={
            "body_type": "mesomorph",
            "fitness_level": "Intermediate",
            "goals": "muscle_gain"
        })
    assert plan.status_code == 200
    
    # Test filter
    exercises = requests.post(f"{base}/api/exercises/filter",
        json={"limit": 5})
    assert exercises.status_code == 200
    
    # Test stats
    stats = requests.get(f"{base}/api/statistics")
    assert stats.status_code == 200
    
    print("✅ All tests passed!")

test_endpoints()
```

### Using cURL
```bash
# Test script
echo "Testing Chat API..."
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"test"}' \
  -w "\nStatus: %{http_code}\n"

echo "Testing Workout Plan API..."
curl -X POST http://localhost:8000/api/workout-plan \
  -H "Content-Type: application/json" \
  -d '{
    "body_type":"mesomorph",
    "fitness_level":"Intermediate",
    "goals":"muscle_gain"
  }' \
  -w "\nStatus: %{http_code}\n"

echo "Testing Filter API..."
curl -X POST http://localhost:8000/api/exercises/filter \
  -H "Content-Type: application/json" \
  -d '{"limit":5}' \
  -w "\nStatus: %{http_code}\n"

echo "Testing Statistics API..."
curl -X GET http://localhost:8000/api/statistics \
  -w "\nStatus: %{http_code}\n"
```

---

## 📚 Additional Resources

- **Swagger UI**: http://localhost:8000/docs (Interactive API testing)
- **ReDoc**: http://localhost:8000/redoc (Alternative API docs)
- **Source Code**: See `app.py` for implementation details
- **RAG System**: See `rag_system.py` for AI logic

---

## 💡 Best Practices

1. **Rate Limiting**: Implement rate limiting in production
2. **Error Handling**: Always check response status codes
3. **Timeouts**: Set appropriate timeouts for requests
4. **Caching**: Cache frequent requests (e.g., statistics)
5. **Authentication**: Add auth for production use
6. **CORS**: Configure CORS for web apps

---

## 🔧 Configuration

Server runs on:
- Host: `0.0.0.0` (all interfaces)
- Port: `8000`

To change port, edit `app.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Change to 8080
```

---

**📞 Need help? Check the main README.md or open an issue!**

