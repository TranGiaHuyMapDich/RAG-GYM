// Global variables
let currentTab = 'chat';
let CURRENT_USER_ID = localStorage.getItem('userId') || null;
let CURRENT_SESSION_ID = localStorage.getItem('sessionId') || generateUUID();
let CURRENT_USER_NAME = null;

// Helper function to generate UUID
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Save session ID
localStorage.setItem('sessionId', CURRENT_SESSION_ID);

// Load user info when page loads
async function loadUserInfo() {
    const userGreeting = document.getElementById('user-greeting');
    const userNameDisplay = document.getElementById('user-name-display');
    const logoutBtn = document.getElementById('logout-btn');
    const loginLink = document.getElementById('login-link');
    
    if (CURRENT_USER_ID) {
        try {
            const response = await fetch(`/api/users/${CURRENT_USER_ID}`);
            if (response.ok) {
                const data = await response.json();
                CURRENT_USER_NAME = data.user.full_name || data.user.email;
                
                // Hiển thị tên user
                userNameDisplay.textContent = CURRENT_USER_NAME;
                userGreeting.style.display = 'block';
                logoutBtn.style.display = 'block';
                loginLink.style.display = 'none';
                
                // Cập nhật welcome message
                updateWelcomeMessage();
            } else {
                // User không tồn tại, xóa localStorage
                localStorage.removeItem('userId');
                CURRENT_USER_ID = null;
                showLoginButton();
            }
        } catch (error) {
            console.error('Error loading user info:', error);
            showLoginButton();
        }
    } else {
        showLoginButton();
    }
}

// Show login button
function showLoginButton() {
    document.getElementById('user-greeting').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'none';
    document.getElementById('login-link').style.display = 'block';
}

// Update welcome message based on login status
function updateWelcomeMessage() {
    const welcomeSection = document.querySelector('.welcome-section h2');
    if (welcomeSection && CURRENT_USER_NAME) {
        welcomeSection.textContent = `🤖 Xin chào ${CURRENT_USER_NAME}! Tôi là trợ lý gym AI của bạn`;
    }
}

// Logout function
function logout() {
    if (confirm('Bạn có chắc muốn đăng xuất?')) {
        localStorage.removeItem('userId');
        localStorage.removeItem('rememberMe');
        CURRENT_USER_ID = null;
        CURRENT_USER_NAME = null;
        
        showNotification('Đã đăng xuất!', 'success');
        
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    loadUserInfo();
});

// Translation functionality
async function translateExercise(cardId, exercise) {
    const card = document.getElementById(cardId);
    if (!card) return;
    
    const btn = card.querySelector('.translate-btn');
    const originalBtnText = btn.innerHTML;
    
    // Show loading
    btn.innerHTML = '⏳ Đang dịch...';
    btn.disabled = true;
    
    try {
        const response = await fetch('/api/translate-exercise', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(exercise)
        });
        
        const data = await response.json();
        
        if (data.success && data.exercise) {
            const ex = data.exercise;
            
            // Update card content with translated text
            const titleEl = card.querySelector('.exercise-title');
            const bodypartEl = card.querySelector('.exercise-bodypart');
            const equipmentEl = card.querySelector('.exercise-equipment');
            const levelEl = card.querySelector('.exercise-level');
            
            // Store original text
            if (!titleEl.dataset.original) {
                titleEl.dataset.original = titleEl.textContent;
                bodypartEl.dataset.original = bodypartEl.textContent;
                equipmentEl.dataset.original = equipmentEl.textContent;
                levelEl.dataset.original = levelEl.textContent;
            }
            
            // Toggle between translated and original
            if (btn.dataset.translated === 'true') {
                // Show original
                titleEl.textContent = titleEl.dataset.original;
                bodypartEl.textContent = bodypartEl.dataset.original;
                equipmentEl.textContent = equipmentEl.dataset.original;
                levelEl.textContent = levelEl.dataset.original;
                btn.innerHTML = '🌐 Dịch sang Tiếng Việt';
                btn.dataset.translated = 'false';
            } else {
                // Show translated
                titleEl.textContent = ex.title_vi || ex.title;
                bodypartEl.textContent = '💪 ' + (ex.bodypart_vi || ex.bodypart);
                equipmentEl.textContent = '🏋️ ' + (ex.equipment_vi || ex.equipment);
                levelEl.textContent = '📊 ' + (ex.level_vi || ex.level);
                btn.innerHTML = '🌐 Hiện Tiếng Anh';
                btn.dataset.translated = 'true';
            }
        } else {
            throw new Error('Translation failed');
        }
    } catch (error) {
        console.error('Translation error:', error);
        showNotification('❌ Không thể dịch. Vui lòng thử lại!', 'error');
        btn.innerHTML = originalBtnText;
    } finally {
        btn.disabled = false;
    }
}

// Tab switching
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
    
    currentTab = tabName;
    
    // Load data for specific tabs
    if (tabName === 'stats') {
        loadStatistics();
    } else if (tabName === 'exercises') {
        loadFilterOptions();
    }
}

// Chat functionality
function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const question = input.value.trim();
    
    if (!question) return;
    
    // Add user message to chat
    addMessage('user', question);
    
    // Clear input
    input.value = '';
    
    // Show loading
    const loadingId = addMessage('bot', 'Đang suy nghĩ...');
    
    try {
        // Call API with user_id for saving history
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                n_results: 5,
                user_id: CURRENT_USER_ID,  // Auto save if user logged in
                session_id: CURRENT_SESSION_ID
            })
        });
        
        const data = await response.json();
        
        // Remove loading message
        removeMessage(loadingId);
        
        // Add bot response
        addMessage('bot', data.answer, data.exercises);
        
    } catch (error) {
        removeMessage(loadingId);
        addMessage('bot', '❌ Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại!');
        console.error('Error:', error);
    }
}

function addMessage(type, text, exercises = null) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageId = 'msg-' + Date.now();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.id = messageId;
    
    let content = `
        <div class="message-header">
            ${type === 'user' ? '👤 Bạn' : '🤖 AI Assistant'}
        </div>
        <div class="message-content">
            ${text.replace(/\n/g, '<br>')}
        </div>
    `;
    
    // Add exercises if available
    if (exercises && exercises.length > 0) {
        content += '<div class="exercises-grid">';
        exercises.forEach((ex, index) => {
            const cardId = `exercise-${messageId}-${index}`;
            content += `
                <div class="exercise-card" id="${cardId}">
                    <h4 class="exercise-title">${ex.title}</h4>
                    <div class="meta">
                        <span class="exercise-bodypart">💪 ${ex.bodypart}</span>
                        <span class="exercise-equipment">🏋️ ${ex.equipment}</span>
                        <span class="exercise-level">📊 ${ex.level}</span>
                        ${ex.rating && ex.rating !== 'nan' ? `<span>⭐ ${ex.rating}</span>` : ''}
                    </div>
                    <button 
                        class="translate-btn" 
                        onclick="translateExercise('${cardId}', ${JSON.stringify(ex).replace(/"/g, '&quot;')})"
                        style="margin-top: 10px; padding: 6px 12px; background: rgba(255, 201, 60, 0.2); border: 1px solid rgba(255, 201, 60, 0.3); color: #ffc93c; border-radius: 8px; cursor: pointer; font-size: 0.85rem; transition: all 0.3s;">
                        🌐 Dịch sang Tiếng Việt
                    </button>
                </div>
            `;
        });
        content += '</div>';
    }
    
    messageDiv.innerHTML = content;
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageId;
}

function removeMessage(messageId) {
    const message = document.getElementById(messageId);
    if (message) {
        message.remove();
    }
}

// Workout Plan functionality
document.getElementById('workout-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const bodyType = document.getElementById('body-type').value;
    const fitnessLevel = document.getElementById('fitness-level').value;
    const goals = document.getElementById('goals').value;
    const daysPerWeek = parseInt(document.getElementById('days-per-week').value);
    const height = parseFloat(document.getElementById('height').value) || null;
    const weight = parseFloat(document.getElementById('weight').value) || null;
    const age = parseInt(document.getElementById('age').value) || null;
    
    // Get selected equipment
    const equipmentSelect = document.getElementById('equipment');
    const selectedEquipment = Array.from(equipmentSelect.selectedOptions).map(opt => opt.value);
    
    if (!bodyType || !fitnessLevel || !goals) {
        alert('Vui lòng điền đầy đủ thông tin bắt buộc!');
        return;
    }
    
    // Show loading
    const resultDiv = document.getElementById('workout-plan-result');
    resultDiv.innerHTML = '<div class="loading">Đang tạo kế hoạch tập luyện...</div>';
    
    try {
        const response = await fetch('/api/workout-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                body_type: bodyType,
                fitness_level: fitnessLevel,
                goals: goals,
                available_equipment: selectedEquipment.length > 0 ? selectedEquipment : null,
                days_per_week: daysPerWeek,
                height: height,
                weight: weight,
                age: age,
                user_id: CURRENT_USER_ID,  // Auto save to database
                plan_name: `Plan ${new Date().toLocaleDateString('vi-VN')}`
            })
        });
        
        const plan = await response.json();
        
        // Display plan
        displayWorkoutPlan(plan);
        
        // Show save notification if saved
        if (plan.saved_plan_id) {
            showNotification('✅ Kế hoạch đã được lưu vào database!', 'success');
        } else if (CURRENT_USER_ID) {
            showNotification('⚠️ Kế hoạch không được lưu', 'warning');
        }
        
        // Scroll to result
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
    } catch (error) {
        resultDiv.innerHTML = '<div class="error">❌ Có lỗi xảy ra khi tạo kế hoạch. Vui lòng thử lại!</div>';
        console.error('Error:', error);
    }
});

function displayWorkoutPlan(plan) {
    const resultDiv = document.getElementById('workout-plan-result');
    
    let html = `
        <div class="plan-header">
            <h3>🎯 Kế Hoạch Tập Luyện Của Bạn</h3>
            <p>📅 ${plan.days_per_week} ngày/tuần - 💪 ${plan.fitness_level} - 🎯 ${plan.goals}</p>
    `;
    
    // User info
    if (plan.user_info && plan.user_info.bmi) {
        html += `
            <div class="user-info">
                ${plan.user_info.height ? `<div class="info-item">
                    <div class="label">Chiều cao</div>
                    <div class="value">${plan.user_info.height} cm</div>
                </div>` : ''}
                ${plan.user_info.weight ? `<div class="info-item">
                    <div class="label">Cân nặng</div>
                    <div class="value">${plan.user_info.weight} kg</div>
                </div>` : ''}
                ${plan.user_info.age ? `<div class="info-item">
                    <div class="label">Tuổi</div>
                    <div class="value">${plan.user_info.age}</div>
                </div>` : ''}
                ${plan.user_info.bmi ? `<div class="info-item">
                    <div class="label">BMI</div>
                    <div class="value">${plan.user_info.bmi}</div>
                </div>` : ''}
                ${plan.user_info.bmi_category ? `<div class="info-item">
                    <div class="label">Phân loại</div>
                    <div class="value">${plan.user_info.bmi_category}</div>
                </div>` : ''}
            </div>
        `;
    }
    
    html += '</div>';
    
    // Recommendations
    if (plan.recommendations && plan.recommendations.length > 0) {
        html += `
            <div class="recommendations">
                <h4>💡 Lời Khuyên Dành Cho Bạn</h4>
                <ul>
                    ${plan.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Weekly plan
    if (plan.weekly_plan && plan.weekly_plan.length > 0) {
        plan.weekly_plan.forEach(day => {
            html += `
                <div class="day-plan">
                    <h4>📅 Ngày ${day.day} - ${day.focus}</h4>
                    <div class="day-exercises">
            `;
            
            if (day.exercises && day.exercises.length > 0) {
                day.exercises.forEach(ex => {
                    html += `
                        <div class="exercise-card">
                            <h4>${ex.metadata.title}</h4>
                            <div class="meta">
                                <span>💪 ${ex.metadata.bodypart}</span>
                                <span>🏋️ ${ex.metadata.equipment}</span>
                                <span>📊 ${ex.metadata.level}</span>
                                ${ex.metadata.rating && ex.metadata.rating !== 'nan' ? `<span>⭐ ${ex.metadata.rating}</span>` : ''}
                            </div>
                        </div>
                    `;
                });
            } else {
                html += '<p>Không tìm thấy bài tập phù hợp. Hãy thử với thiết bị khác.</p>';
            }
            
            html += `
                    </div>
                </div>
            `;
        });
    }
    
    resultDiv.innerHTML = html;
}

// Exercise filter functionality
async function loadFilterOptions() {
    try {
        // Load body parts
        const bodyPartsResponse = await fetch('/api/body-parts');
        const bodyPartsData = await bodyPartsResponse.json();
        const bodyPartSelect = document.getElementById('filter-bodypart');
        bodyPartsData.body_parts.forEach(bp => {
            if (bp) {
                const option = document.createElement('option');
                option.value = bp;
                option.textContent = bp;
                bodyPartSelect.appendChild(option);
            }
        });
        
        // Load equipment
        const equipmentResponse = await fetch('/api/equipment');
        const equipmentData = await equipmentResponse.json();
        const equipmentSelect = document.getElementById('filter-equipment');
        equipmentData.equipment.forEach(eq => {
            if (eq) {
                const option = document.createElement('option');
                option.value = eq;
                option.textContent = eq;
                equipmentSelect.appendChild(option);
            }
        });
        
    } catch (error) {
        console.error('Error loading filter options:', error);
    }
}

async function searchExercises() {
    const bodyPart = document.getElementById('filter-bodypart').value;
    const equipment = document.getElementById('filter-equipment').value;
    const level = document.getElementById('filter-level').value;
    
    const resultDiv = document.getElementById('exercises-result');
    resultDiv.innerHTML = '<div class="loading">Đang tìm kiếm...</div>';
    
    try {
        const response = await fetch('/api/exercises/filter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                body_part: bodyPart || null,
                equipment: equipment || null,
                level: level || null,
                limit: 20
            })
        });
        
        const data = await response.json();
        
        displayExercises(data.exercises, data.total);
        
    } catch (error) {
        resultDiv.innerHTML = '<div class="error">❌ Có lỗi xảy ra khi tìm kiếm. Vui lòng thử lại!</div>';
        console.error('Error:', error);
    }
}

function displayExercises(exercises, total) {
    const resultDiv = document.getElementById('exercises-result');
    
    if (exercises.length === 0) {
        resultDiv.innerHTML = '<p>Không tìm thấy bài tập nào phù hợp.</p>';
        return;
    }
    
    let html = `
        <div class="result-header">
            <h3>🔍 Tìm thấy ${total} bài tập</h3>
        </div>
        <div class="exercises-grid">
    `;
    
    exercises.forEach(ex => {
        html += `
            <div class="exercise-card">
                <h4>${ex.title}</h4>
                <p style="font-size: 0.9rem; margin: 0.5rem 0; color: var(--text-secondary);">
                    ${ex.description.substring(0, 150)}${ex.description.length > 150 ? '...' : ''}
                </p>
                <div class="meta">
                    <span>🎯 ${ex.type}</span>
                    <span>💪 ${ex.bodypart}</span>
                    <span>🏋️ ${ex.equipment}</span>
                    <span>📊 ${ex.level}</span>
                    ${ex.rating && ex.rating !== 'nan' ? `<span>⭐ ${ex.rating}</span>` : ''}
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    
    resultDiv.innerHTML = html;
}

// Statistics functionality
async function loadStatistics() {
    const statsContent = document.getElementById('stats-content');
    statsContent.innerHTML = '<div class="loading">Đang tải thống kê...</div>';
    
    try {
        const response = await fetch('/api/statistics');
        const stats = await response.json();
        
        displayStatistics(stats);
        
    } catch (error) {
        statsContent.innerHTML = '<div class="error">❌ Có lỗi xảy ra khi tải thống kê.</div>';
        console.error('Error:', error);
    }
}

function displayStatistics(stats) {
    const statsContent = document.getElementById('stats-content');
    
    let html = `
        <div class="stat-category">
            <h3>📊 Tổng Quan</h3>
            <div class="stat-grid">
                <div class="stat-item">
                    <div class="stat-label">Tổng Bài Tập</div>
                    <div class="stat-value">${stats.total_exercises}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Nhóm Cơ</div>
                    <div class="stat-value">${Object.keys(stats.body_parts).length}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Loại Thiết Bị</div>
                    <div class="stat-value">${Object.keys(stats.equipment_types).length}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Cấp Độ</div>
                    <div class="stat-value">${Object.keys(stats.levels).length}</div>
                </div>
            </div>
        </div>
    `;
    
    // Body Parts
    html += `
        <div class="stat-category">
            <h3>💪 Top Nhóm Cơ</h3>
            <div class="stat-grid">
    `;
    
    const topBodyParts = Object.entries(stats.body_parts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
    
    topBodyParts.forEach(([name, count]) => {
        html += `
            <div class="stat-item">
                <div class="stat-label">${name}</div>
                <div class="stat-value">${count}</div>
            </div>
        `;
    });
    
    html += '</div></div>';
    
    // Equipment
    html += `
        <div class="stat-category">
            <h3>🏋️ Top Thiết Bị</h3>
            <div class="stat-grid">
    `;
    
    const topEquipment = Object.entries(stats.equipment_types)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
    
    topEquipment.forEach(([name, count]) => {
        html += `
            <div class="stat-item">
                <div class="stat-label">${name}</div>
                <div class="stat-value">${count}</div>
            </div>
        `;
    });
    
    html += '</div></div>';
    
    // Levels
    html += `
        <div class="stat-category">
            <h3>📊 Phân Bố Cấp Độ</h3>
            <div class="stat-grid">
    `;
    
    Object.entries(stats.levels).forEach(([name, count]) => {
        html += `
            <div class="stat-item">
                <div class="stat-label">${name}</div>
                <div class="stat-value">${count}</div>
            </div>
        `;
    });
    
    html += '</div></div>';
    
    // Types
    html += `
        <div class="stat-category">
            <h3>🎯 Loại Bài Tập</h3>
            <div class="stat-grid">
    `;
    
    Object.entries(stats.types).forEach(([name, count]) => {
        html += `
            <div class="stat-item">
                <div class="stat-label">${name}</div>
                <div class="stat-value">${count}</div>
            </div>
        `;
    });
    
    html += '</div></div>';
    
    statsContent.innerHTML = html;
}

// User management functions
async function quickRegister() {
    const email = prompt('Nhập email của bạn:');
    if (!email) return;
    
    const name = prompt('Nhập tên của bạn:') || 'User';
    
    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                full_name: name,
                body_type: 'mesomorph',
                fitness_level: 'Beginner',
                primary_goal: 'general_fitness'
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            setUserId(data.user.id);
            showNotification('✅ Đăng ký thành công! Dữ liệu của bạn sẽ được lưu.', 'success');
            updateUserStatus();
        } else {
            const error = await response.json();
            showNotification('❌ ' + (error.detail || 'Đăng ký thất bại'), 'error');
        }
    } catch (error) {
        showNotification('❌ Lỗi kết nối. Supabase chưa được cấu hình.', 'error');
    }
}

// Old functions removed - using new user system with loadUserInfo()

async function viewMyData() {
    if (!CURRENT_USER_ID) {
        showNotification('⚠️ Vui lòng đăng ký trước', 'warning');
        return;
    }
    
    try {
        // Get user stats
        const statsResponse = await fetch(`/api/users/${CURRENT_USER_ID}/stats`);
        const statsData = await statsResponse.json();
        
        // Get workout plans
        const plansResponse = await fetch(`/api/users/${CURRENT_USER_ID}/workout-plans`);
        const plansData = await plansResponse.json();
        
        // Get favorites
        const favsResponse = await fetch(`/api/users/${CURRENT_USER_ID}/favorites`);
        const favsData = await favsResponse.json();
        
        // Display in modal or new section
        let html = `
            <div style="background: var(--card-bg); padding: 20px; border-radius: 15px; margin: 20px 0;">
                <h3 style="color: var(--secondary-color); margin-bottom: 15px;">📊 Dữ Liệu Của Bạn</h3>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px;">
                    <div style="background: var(--dark-bg); padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 2rem; color: var(--primary-color);">${statsData.stats.total_plans || 0}</div>
                        <div style="color: var(--text-secondary);">Kế hoạch tập</div>
                    </div>
                    <div style="background: var(--dark-bg); padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 2rem; color: var(--warning);">${statsData.stats.total_favorites || 0}</div>
                        <div style="color: var(--text-secondary);">Bài tập yêu thích</div>
                    </div>
                </div>
                
                <h4 style="color: var(--text-primary); margin: 20px 0 10px;">📋 Kế hoạch đã lưu:</h4>
                <div style="max-height: 300px; overflow-y: auto;">
        `;
        
        if (plansData.plans && plansData.plans.length > 0) {
            plansData.plans.forEach(plan => {
                html += `
                    <div style="background: var(--dark-bg); padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid var(--secondary-color);">
                        <div style="font-weight: bold;">${plan.plan_name}</div>
                        <div style="font-size: 0.9rem; color: var(--text-secondary);">
                            ${plan.days_per_week} ngày/tuần - ${new Date(plan.created_at).toLocaleDateString('vi-VN')}
                        </div>
                    </div>
                `;
            });
        } else {
            html += '<p style="color: var(--text-secondary);">Chưa có kế hoạch nào được lưu.</p>';
        }
        
        html += `
                </div>
                <button onclick="closeMyData()" style="margin-top: 15px; padding: 10px 20px; background: var(--primary-color); border: none; border-radius: 8px; color: white; cursor: pointer;">Đóng</button>
            </div>
        `;
        
        const container = document.createElement('div');
        container.id = 'my-data-modal';
        container.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 1000; max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto; background: var(--light-bg); padding: 20px; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.5);';
        container.innerHTML = html;
        
        const overlay = document.createElement('div');
        overlay.id = 'modal-overlay';
        overlay.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); z-index: 999;';
        overlay.onclick = closeMyData;
        
        document.body.appendChild(overlay);
        document.body.appendChild(container);
        
    } catch (error) {
        showNotification('❌ Không thể tải dữ liệu', 'error');
        console.error(error);
    }
}

function closeMyData() {
    const modal = document.getElementById('my-data-modal');
    const overlay = document.getElementById('modal-overlay');
    if (modal) modal.remove();
    if (overlay) overlay.remove();
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: ${type === 'success' ? '#4ecca3' : type === 'error' ? '#ff6b6b' : type === 'warning' ? '#ffc93c' : '#4ecdc4'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        max-width: 300px;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('🏋️ Gym RAG AI Assistant initialized!');
    
    // Update user status
    updateUserStatus();
    
    // Add welcome message
    const welcomeMsg = CURRENT_USER_ID 
        ? `Xin chào! 👋

Tôi là trợ lý gym AI của bạn, được huấn luyện trên hơn 2900+ bài tập gym.

✅ Bạn đã đăng nhập - Dữ liệu sẽ được lưu tự động!

Tôi có thể giúp bạn:
✅ Tìm bài tập phù hợp
✅ Tạo kế hoạch tập luyện cá nhân
✅ Tư vấn kỹ thuật tập luyện
✅ Gợi ý dựa trên trang người và mục tiêu

Hãy bắt đầu bằng cách hỏi tôi bất cứ điều gì về gym! 💪`
        : `Xin chào! 👋

Tôi là trợ lý gym AI của bạn, được huấn luyện trên hơn 2900+ bài tập gym.

⚠️ Bạn chưa đăng nhập - Click "Đăng ký nhanh" để lưu dữ liệu!

Tôi có thể giúp bạn:
✅ Tìm bài tập phù hợp
✅ Tạo kế hoạch tập luyện cá nhân
✅ Tư vấn kỹ thuật tập luyện
✅ Gợi ý dựa trên trang người và mục tiêu

Hãy bắt đầu bằng cách hỏi tôi bất cứ điều gì về gym! 💪`;
    
    addMessage('bot', welcomeMsg);
});

