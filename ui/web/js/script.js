// ui/web/js/script.js

let backend; // Will hold the Python backend object

// Initialize QWebChannel
document.addEventListener("DOMContentLoaded", () => {
    if (typeof QWebChannel !== "undefined") {
        new QWebChannel(qt.webChannelTransport, (channel) => {
            // 'backend' matches the name registered in Python
            backend = channel.objects.backend;

            // Initialize data
            initDashboard();
        });
    } else {
        console.error("QWebChannel not found. Are you running inside the Python app?");
    }
});

function initDashboard() {
    if (!backend) return;

    // Example: Fetch user info
    backend.get_user_info((infoStr) => {
        // info is a JSON object or string returned from Python
        if (infoStr) {
            const info = JSON.parse(infoStr);
            document.getElementById("username-display").textContent = info.username;
            document.getElementById("user-avatar").textContent = info.username.charAt(0).toUpperCase();

            // Populate settings if fields are there
            const uField = document.getElementById("setting-username");
            if (uField) uField.value = info.username;
        }
    });

    console.log("Dashboard initialized via Python bridge.");
}

// Navigation Logic
function activateNav(element, viewName) {
    // 1. visual update sidebar
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    element.classList.add('active');

    // 2. update title
    const titles = {
        'dashboard': 'Dashboard',
        'projects': 'Project Management',
        'financials': 'Financial Overview',
        'settings': 'Settings'
    };
    document.getElementById('page-title').textContent = titles[viewName] || 'Dashboard';

    // 3. toggle views (simple implementation)
    // Hide all first
    document.getElementById('dashboard-view').style.display = 'none';
    const pView = document.getElementById('projects-view');
    if (pView) pView.style.display = 'none';
    const sView = document.getElementById('settings-view');
    if (sView) sView.style.display = 'none';

    // Show target
    const target = document.getElementById(viewName + '-view');
    if (target) {
        target.style.display = 'block';
        target.style.animation = 'fadeIn 0.5s ease-out';
    }

    // 4. Notify backend
    if (backend) {
        backend.log_navigation(viewName);
    }
}

// --- SETTINGS LOGIC ---
function saveProfile() {
    const password = document.getElementById('setting-password').value;

    // In a real app, handle file upload differently. 
    // Here we just mock it or send a signal to Python to open a file dialog if needed.

    if (backend) {
        backend.update_profile(password, (response) => {
            alert(response);
            document.getElementById('setting-password').value = ""; // clear
        });
    }
}

function triggerDbReset() {
    if (confirm("Are you sure? This will delete all data and close the app.")) {
        if (backend) backend.reset_database();
    }
}
