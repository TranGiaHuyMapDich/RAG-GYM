// Auth.js - Login & Registration Logic

const API_BASE = window.location.origin;

// Switch between Login and Register tabs
function switchTab(tab) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const tabs = document.querySelectorAll('.tab-btn');

    tabs.forEach(btn => btn.classList.remove('active'));

    if (tab === 'login') {
        loginForm.classList.add('active');
        registerForm.classList.remove('active');
        tabs[0].classList.add('active');
    } else {
        registerForm.classList.add('active');
        loginForm.classList.remove('active');
        tabs[1].classList.add('active');
    }
}

// Show/Hide loading overlay
function showLoading(show = true) {
    const overlay = document.getElementById('loading-overlay');
    if (show) {
        overlay.classList.add('active');
    } else {
        overlay.classList.remove('active');
    }
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Handle Login
async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('login-email').value.trim();
    const rememberMe = document.getElementById('remember-me').checked;

    if (!email) {
        showNotification('Vui lòng nhập email!', 'error');
        return;
    }

    showLoading(true);

    try {
        // Try to find existing user by email
        const response = await fetch(`${API_BASE}/api/users/by-email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        });

        if (response.ok) {
            const data = await response.json();
            
            if (data.user) {
                // User found - login success
                localStorage.setItem('userId', data.user.id);
                if (rememberMe) {
                    localStorage.setItem('rememberMe', 'true');
                }
                
                showNotification('✅ Đăng nhập thành công!', 'success');
                
                // Redirect to main page after 1 second
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                showNotification('❌ Email không tồn tại! Vui lòng đăng ký.', 'error');
            }
        } else {
            showNotification('❌ Email không tồn tại! Vui lòng đăng ký.', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('❌ Lỗi kết nối. Vui lòng thử lại!', 'error');
    } finally {
        showLoading(false);
    }
}

// Handle Registration
async function handleRegister(event) {
    event.preventDefault();

    // Get form values - chỉ cần email và tên
    const email = document.getElementById('register-email').value.trim();
    const name = document.getElementById('register-name').value.trim();

    // Validation
    if (!email || !name) {
        showNotification('Vui lòng điền đầy đủ email và tên!', 'error');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE}/api/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                full_name: name
            })
        });

        if (response.ok) {
            const data = await response.json();
            
            showNotification('✅ Đăng ký thành công! Đang chuyển sang trang đăng nhập...', 'success');
            
            // Chuyển sang tab đăng nhập sau 1.5 giây
            setTimeout(() => {
                switchTab('login');
                document.getElementById('login-email').value = email;
                document.getElementById('login-email').focus();
            }, 1500);
        } else {
            const error = await response.json();
            if (error.detail && error.detail.includes('already exists')) {
                showNotification('❌ Email đã tồn tại! Đang chuyển sang đăng nhập...', 'error');
                // Switch to login tab
                setTimeout(() => {
                    switchTab('login');
                    document.getElementById('login-email').value = email;
                }, 1500);
            } else {
                showNotification('❌ ' + (error.detail || 'Đăng ký thất bại!'), 'error');
            }
        }
    } catch (error) {
        console.error('Registration error:', error);
        showNotification('❌ Lỗi kết nối. Vui lòng thử lại!', 'error');
    } finally {
        showLoading(false);
    }
}

// Check if already logged in on page load
window.addEventListener('DOMContentLoaded', () => {
    const userId = localStorage.getItem('userId');
    
    if (userId) {
        // Already logged in - redirect to main page
        showNotification('Bạn đã đăng nhập. Đang chuyển hướng...', 'success');
        setTimeout(() => {
            window.location.href = '/';
        }, 1000);
    }
});

// Form auto-fill from URL params (if coming from "quick register")
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('email')) {
    document.getElementById('register-email').value = urlParams.get('email');
    switchTab('register');
}

