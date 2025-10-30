# 📁 Tổng Quan Dự Án - Gym RAG AI Assistant

## 🎯 Mô Tả Dự Án

Một hệ thống **RAG (Retrieval Augmented Generation) AI** hoàn chỉnh cho lĩnh vực gym, cung cấp:
- ✅ Chat AI thông minh về gym và tập luyện
- ✅ Tạo kế hoạch tập luyện cá nhân hóa theo trang người và mục tiêu
- ✅ Tìm kiếm và lọc hơn 2900+ bài tập
- ✅ Phân tích BMI và đưa ra lời khuyên sức khỏe
- ✅ Web interface hiện đại và responsive

---

## 📂 Cấu Trúc Thư Mục

```
RAG GYM/
├── 📄 app.py                    # FastAPI web server (backend chính)
├── 📄 rag_system.py             # RAG engine với ChromaDB
├── 📄 requirements.txt          # Dependencies Python
├── 📄 start.py                  # Script khởi chạy thông minh
├── 📄 start.bat                 # Batch file cho Windows (khởi chạy)
├── 📄 run.bat                   # Batch file cho Windows (chạy nhanh)
├── 📄 megaGymDataset.csv        # Dataset 2920 bài tập
├── 📄 README.md                 # Tài liệu đầy đủ
├── 📄 QUICKSTART.md             # Hướng dẫn nhanh
├── 📄 .gitignore                # Git ignore file
└── 📁 static/                   # Frontend files
    ├── index.html               # Giao diện chính
    ├── styles.css               # Styling (dark theme)
    └── script.js                # JavaScript logic
```

---

## 🚀 Cách Chạy Ứng Dụng

### Option 1: Sử dụng Start Script (Khuyến nghị)
```bash
python start.py
```
Hoặc double-click `start.bat` (Windows)

### Option 2: Chạy Trực Tiếp
```bash
python app.py
```
Hoặc double-click `run.bat` (Windows)

### Option 3: Từng Bước
```bash
# Bước 1: Cài dependencies
pip install -r requirements.txt

# Bước 2: Chạy app
python app.py
```

### Truy Cập
- 🌐 Web App: **http://localhost:8000**
- 📚 API Docs: **http://localhost:8000/docs**

---

## 🧩 Chi Tiết Các Thành Phần

### 1. **app.py** - FastAPI Backend

**Chức năng:**
- Web server chính sử dụng FastAPI
- Định nghĩa tất cả API endpoints
- Xử lý requests từ frontend
- Tích hợp với RAG system

**Các API Endpoints:**
- `GET /` - Trang chủ
- `POST /api/chat` - Chat với AI
- `POST /api/workout-plan` - Tạo kế hoạch tập
- `POST /api/exercises/filter` - Lọc bài tập
- `GET /api/statistics` - Thống kê dataset
- `GET /api/body-parts` - Danh sách nhóm cơ
- `GET /api/equipment` - Danh sách thiết bị

**Công nghệ:**
- FastAPI (modern Python web framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)

### 2. **rag_system.py** - RAG Engine

**Chức năng:**
- Core RAG system xử lý AI logic
- Load và process dataset CSV
- Tạo embeddings cho semantic search
- Lưu trữ vectors trong ChromaDB
- Tìm kiếm theo ngữ nghĩa
- Tạo kế hoạch tập luyện cá nhân hóa

**Các Class và Methods Chính:**

```python
class GymRAGSystem:
    def __init__(csv_path)                    # Khởi tạo RAG
    def load_data()                           # Load CSV data
    def create_documents()                    # Tạo documents
    def initialize_vector_store()             # Tạo vector DB
    def search(query, n_results, filters)     # Semantic search
    def generate_workout_plan(...)            # Tạo kế hoạch tập
    def get_exercise_by_filters(...)          # Lọc bài tập
    def get_statistics()                      # Thống kê
```

**Công nghệ:**
- ChromaDB (vector database)
- Sentence Transformers (embeddings model)
- Pandas (data processing)

**Model Sử Dụng:**
- `paraphrase-multilingual-mpnet-base-v2`
- Hỗ trợ tiếng Việt và tiếng Anh
- Embedding dimension: 768
- Size: ~420MB

### 3. **Frontend (static/)** - Web Interface

#### **index.html**
- Cấu trúc HTML5 semantic
- 4 tabs chính: Chat, Workout Plan, Exercises, Stats
- Responsive layout
- Forms với validation

#### **styles.css**
- Modern dark theme
- CSS3 animations và transitions
- Gradient backgrounds
- Responsive design (mobile-friendly)
- Custom scrollbar
- Card-based layouts

**Design Tokens:**
```css
--primary-color: #ff6b6b    (Đỏ cam)
--secondary-color: #4ecdc4  (Xanh mint)
--dark-bg: #1a1a2e          (Nền tối)
--gradient-1: Purple gradient
--gradient-2: Pink gradient
--gradient-3: Blue gradient
```

#### **script.js**
- Vanilla JavaScript (no frameworks)
- Event handling
- API calls với Fetch
- DOM manipulation
- Real-time chat interface
- Dynamic content rendering

**Key Functions:**
```javascript
showTab(tabName)              // Chuyển tab
sendMessage()                 // Gửi chat message
createWorkoutPlan()           // Tạo kế hoạch tập
searchExercises()             // Tìm bài tập
loadStatistics()              // Load thống kê
```

### 4. **Dataset (megaGymDataset.csv)**

**Thông tin:**
- 2920 bài tập gym
- 9 columns: id, Title, Desc, Type, BodyPart, Equipment, Level, Rating, RatingDesc

**Phân bố:**
- Body Parts: 14+ nhóm cơ (Chest, Back, Legs, etc.)
- Equipment: 10+ loại (Barbell, Dumbbell, Machine, etc.)
- Levels: Beginner, Intermediate, Advanced
- Types: Strength, Cardio, Stretching, etc.

---

## 🎨 Tính Năng Nổi Bật

### 1. **Semantic Search (Tìm kiếm ngữ nghĩa)**
- Không cần từ khóa chính xác
- Hiểu ý nghĩa câu hỏi
- Tìm bài tập liên quan nhất
- Hỗ trợ tiếng Việt

**Ví dụ:**
- "Bài tập ngực cho người mới" → Tìm chest exercises cho Beginner
- "Tập lưng với tạ đơn" → Back exercises với Dumbbell
- "Làm sao để tăng cơ tay" → Biceps/Triceps exercises

### 2. **Personalized Workout Plans**

**Input:**
- Body Type: Ectomorph/Mesomorph/Endomorph
- Fitness Level: Beginner/Intermediate/Advanced
- Goals: Muscle gain, Weight loss, Strength, Endurance
- Days per week: 3-6 days
- Available equipment
- Optional: Height, Weight, Age

**Output:**
- BMI calculation
- Body type recommendations
- Weekly workout schedule
- Exercise suggestions per day
- Customized advice

**Logic:**
- Different splits based on frequency
  - 3 days: Full body
  - 4 days: Upper/Lower
  - 5 days: Bro split
  - 6 days: Push/Pull/Legs x2
- Exercises matched to equipment
- Level-appropriate suggestions

### 3. **Advanced Filtering**
- Filter by body part
- Filter by equipment
- Filter by level
- Sorted by rating
- Limit results

### 4. **Statistics Dashboard**
- Total exercises count
- Body parts distribution
- Equipment types distribution
- Level distribution
- Exercise types breakdown

---

## 🛠️ Công Nghệ Sử Dụng

### Backend
- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Pandas** - Data processing

### RAG/AI
- **LangChain** - RAG framework
- **ChromaDB** - Vector database
- **Sentence Transformers** - Embeddings
- **NumPy** - Numerical operations

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling
- **JavaScript** - Vanilla JS (no jQuery)

### Dependencies
Xem `requirements.txt` cho phiên bản chi tiết

---

## 💡 Cách Hoạt Động

### Flow 1: Chat Query
```
User Question
    ↓
Frontend (script.js)
    ↓
POST /api/chat
    ↓
FastAPI (app.py)
    ↓
RAG System (rag_system.py)
    ↓
Sentence Transformer → Embedding
    ↓
ChromaDB → Semantic Search
    ↓
Top K Results
    ↓
Return to User
```

### Flow 2: Workout Plan
```
User Info (body type, level, goals...)
    ↓
POST /api/workout-plan
    ↓
RAG System
    ↓
Calculate BMI
    ↓
Determine workout split
    ↓
For each day:
    For each muscle group:
        Search exercises (filtered by level, equipment)
    ↓
Combine into weekly plan
    ↓
Add recommendations
    ↓
Return complete plan
```

### Flow 3: Vector Database Creation
```
CSV File
    ↓
Load with Pandas
    ↓
Create documents (title + desc + metadata)
    ↓
Generate embeddings (Sentence Transformer)
    ↓
Store in ChromaDB
    ↓
Persist to disk (chroma_db/)
```

---

## 📊 Performance

### Initial Load
- First run: 5-10 minutes (download models)
- Vector DB creation: 2-3 minutes (2920 docs)
- Subsequent runs: ~10 seconds

### Query Speed
- Semantic search: ~100-200ms
- Workout plan generation: ~1-2 seconds
- Filter search: ~50-100ms

### Memory Usage
- Models: ~500MB
- ChromaDB: ~200MB
- App runtime: ~100-200MB
- Total: ~1GB

### Storage
- Models cache: ~500MB
- Vector database: ~200MB
- Dataset: ~1.5MB
- Code: ~100KB

---

## 🔒 Security & Best Practices

### Implemented
- ✅ Input validation (Pydantic models)
- ✅ Error handling
- ✅ CORS enabled for localhost
- ✅ No sensitive data exposed
- ✅ Read-only database access

### Recommendations for Production
- [ ] Add authentication
- [ ] Rate limiting
- [ ] HTTPS
- [ ] Environment variables for config
- [ ] Logging to files
- [ ] Database backups
- [ ] API versioning

---

## 🎯 Use Cases

### Personal Trainer
- Tạo kế hoạch cho học viên
- Tìm bài tập thay thế
- Kiểm tra kỹ thuật

### Gym Member
- Tự tạo lịch tập
- Học bài tập mới
- Tìm bài tập theo thiết bị có sẵn

### Fitness Content Creator
- Research bài tập
- Lên kế hoạch content
- Tìm variations

### Gym Owner
- Hỗ trợ khách hàng
- Training cho staff
- Database bài tập

---

## 🚧 Mở Rộng Tương Lai

### Features
- [ ] Nutrition calculator
- [ ] Video tutorials integration
- [ ] Progress tracking
- [ ] Social features (share workouts)
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Voice input
- [ ] Image recognition (form check)

### Technical
- [ ] Deploy to cloud (AWS/Azure/GCP)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Unit tests
- [ ] Load testing
- [ ] Database optimization
- [ ] Caching layer (Redis)
- [ ] CDN for static files

### AI/ML
- [ ] Fine-tune model on gym domain
- [ ] Add LLM for better responses (GPT/Claude)
- [ ] Image-based exercise search
- [ ] Pose estimation for form check
- [ ] Personalized recommendations based on history

---

## 🤝 Đóng Góp

### Code Structure
- Follow PEP 8 for Python
- Comment in Vietnamese or English
- Use type hints
- Write docstrings

### Git Workflow
1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

### Areas to Contribute
- Add more exercises
- Improve UI/UX
- Add new features
- Fix bugs
- Improve documentation
- Translations

---

## 📝 License

MIT License - Free to use for personal and commercial projects

---

## 🙏 Credits

### Technologies
- FastAPI - Sebastián Ramírez
- ChromaDB - Chroma team
- Sentence Transformers - UKPLab
- Dataset - Exercise Database

### Built with ❤️ using Python

---

## 📞 Support

### Gặp vấn đề?
1. Kiểm tra QUICKSTART.md
2. Xem README.md
3. Check logs trong terminal
4. Open issue on GitHub

### Contact
- GitHub Issues
- Email support

---

**🏋️ Happy Training with Gym RAG AI Assistant! 💪**

