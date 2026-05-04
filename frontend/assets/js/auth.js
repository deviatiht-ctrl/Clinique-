/* Authentication Module - Haiti Reh-Care */

function getCurrentUser() {
  const userStr = localStorage.getItem('hrc_user');
  return userStr ? JSON.parse(userStr) : null;
}

function getToken() {
  return localStorage.getItem('hrc_token');
}

function isLoggedIn() {
  return !!getToken();
}

function isAdmin() {
  const user = getCurrentUser();
  return user && user.role === 'admin';
}

function logout() {
  localStorage.removeItem('hrc_token');
  localStorage.removeItem('hrc_user');
  window.location.href = '/pages/login.html';
}

function checkAuth(requiredRole = null) {
  const token = getToken();
  const user = getCurrentUser();
  
  if (!token) {
    window.location.href = '/pages/login.html';
    return false;
  }
  
  if (requiredRole && user?.role !== requiredRole) {
    window.location.href = '/pages/login.html';
    return false;
  }
  
  return true;
}

function updateNavbar() {
  const user = getCurrentUser();
  const userMenu = document.getElementById('userMenu');
  const loginBtn = document.getElementById('loginBtn');
  const adminLink = document.getElementById('adminLink');
  
  if (user) {
    // User is logged in
    if (userMenu) {
      userMenu.style.display = 'block';
      const avatar = document.getElementById('userAvatar');
      if (avatar) {
        avatar.textContent = (user.first_name?.[0] || user.email[0]).toUpperCase();
      }
    }
    if (loginBtn) {
      loginBtn.style.display = 'none';
    }
    
    // Show admin link if admin
    if (adminLink && user.role === 'admin') {
      adminLink.classList.add('visible');
    }
  } else {
    // User is not logged in
    if (userMenu) {
      userMenu.style.display = 'none';
    }
    if (loginBtn) {
      loginBtn.style.display = 'flex';
    }
    if (adminLink) {
      adminLink.classList.remove('visible');
    }
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', updateNavbar);

// Make available globally
window.getCurrentUser = getCurrentUser;
window.getToken = getToken;
window.isLoggedIn = isLoggedIn;
window.isAdmin = isAdmin;
window.logout = logout;
window.checkAuth = checkAuth;
window.updateNavbar = updateNavbar;
