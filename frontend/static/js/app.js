// Global application state
let appState = {
    user: null,
    token: localStorage.getItem('access_token')
};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupHTMXInterceptors();
});

function initializeApp() {
    // Check authentication status
    checkAuthStatus();

    // Setup event listeners
    setupEventListeners();
}

function setupHTMXInterceptors() {
    // Add auth token to all HTMX requests
    document.body.addEventListener('htmx:configRequest', function(event) {
        const token = localStorage.getItem('access_token');
        if (token) {
            event.detail.headers['Authorization'] = 'Bearer ' + token;
        }
    });

    // Handle 401 responses (unauthorized)
    document.body.addEventListener('htmx:responseError', function(event) {
        if (event.detail.xhr.status === 401) {
            handleUnauthorized();
        } else if (event.detail.xhr.status === 403) {
            showToast('Доступ запрещен', 'error');
        }
    });

    // Show loading indicator
    document.body.addEventListener('htmx:beforeRequest', function() {
        showLoading(true);
    });

    document.body.addEventListener('htmx:afterRequest', function() {
        showLoading(false);
    });
}

function setupEventListeners() {
    // Logout functionality
    document.addEventListener('click', function(e) {
        if (e.target.closest('#logout-btn')) {
            e.preventDefault();
            logout();
        }
    });

    // Close toast notifications
    document.addEventListener('click', function(e) {
        if (e.target.closest('.btn-close')) {
            e.target.closest('.toast').remove();
        }
    });
}

function checkAuthStatus() {
    const token = localStorage.getItem('access_token');
    if (token) {
        // Verify token and get user info
        fetch('/api/v1/auth/me', {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
            .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Not authenticated');
        })
            .then(user => {
            appState.user = user;
            updateUIForAuth(user);
        })
            .catch(error => {
            console.error('Auth check failed:', error);
            localStorage.removeItem('access_token');
            appState.token = null;
            appState.user = null;
            updateUIForAuth(null);
        });
    } else {
        updateUIForAuth(null);
    }
}

function updateUIForAuth(user) {
    const authButtons = document.getElementById('auth-buttons');
    const adminActions = document.getElementById('admin-actions');

    if (user) {
        authButtons.innerHTML = `
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                    <i class="fas fa-user"></i> ${user.email}
                </a>
                <ul class="dropdown-menu">
                    ${user.is_admin ? '<li><a class="dropdown-item" href="/admin">Админ панель</a></li>' : ''}
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" id="logout-btn">Выйти</a></li>
                </ul>
            </li>
        `;

        if (user.is_admin && adminActions) {
            adminActions.classList.remove('d-none');
        }
    } else {
        authButtons.innerHTML = `
            <a class="nav-link" href="/login" hx-get="/login" hx-target="main" hx-push-url="true">
                <i class="fas fa-sign-in-alt"></i> Войти
            </a>
        `;

        if (adminActions) {
            adminActions.classList.add('d-none');
        }
    }
}

function handleUnauthorized() {
    localStorage.removeItem('access_token');
    appState.token = null;
    appState.user = null;
    updateUIForAuth(null);
    showToast('Сессия истекла. Пожалуйста, войдите снова.', 'warning');
}

function logout() {
    localStorage.removeItem('access_token');
    appState.token = null;
    appState.user = null;
    updateUIForAuth(null);
    showToast('Вы успешно вышли из системы', 'info');

    // Reload current page
    htmx.ajax('GET', window.location.pathname, { target: 'main', swap: 'innerHTML' });
}

function showLoading(show) {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.classList.toggle('d-none', !show);
    }
}

function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    const toastId = 'toast-' + Date.now();

    const bgClass = {
        'success': 'bg-success',
        'error': 'bg-danger',
        'warning': 'bg-warning',
        'info': 'bg-info'
    }[type] || 'bg-info';

    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);

    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 5000 });
    toast.show();

    // Remove toast from DOM after hide
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU');
}

function formatPoints(points) {
    return points.toLocaleString('ru-RU');
}

// HTMX extensions for better UX
htmx.defineExtension('disable-element', {
    onEvent: function (name, evt) {
        if (name === 'htmx:beforeRequest') {
            const target = evt.detail.target;
            target.disabled = true;
        } else if (name === 'htmx:afterRequest') {
            const target = evt.detail.target;
            target.disabled = false;
        }
    }
});