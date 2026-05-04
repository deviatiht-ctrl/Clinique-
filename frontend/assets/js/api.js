/* API Client - Haiti Reh-Care */

const API_BASE = 'https://your-render-app.onrender.com'; 
// Change to your Render URL — set as const, imported everywhere

const api = {
  // Auth
  login: (email, password) => fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: new URLSearchParams({username: email, password})
  }).then(r => r.json()),
  
  register: (data) => fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(r => r.json()),

  // Appointments
  getSlots: (date) => fetch(`${API_BASE}/appointments/slots?appointment_date=${date}`).then(r => r.json()),
  
  createAppointment: (data) => fetch(`${API_BASE}/appointments/`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(r => r.json()),
  
  // Admin - Appointments
  listAppointments: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return authFetch(`${API_BASE}/appointments/?${qs}`).then(r => r.json());
  },
  
  updateAppointmentStatus: (id, status) => authFetch(`${API_BASE}/appointments/${id}/status`, {
    method: 'PATCH',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({status})
  }).then(r => r.json()),

  // Patients
  registerPatient: (data) => fetch(`${API_BASE}/patients/`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(r => r.json()),
  
  getPatients: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return authFetch(`${API_BASE}/patients/?${qs}`).then(r => r.json());
  },
  
  getPatient: (id) => authFetch(`${API_BASE}/patients/${id}`).then(r => r.json()),
  
  updatePatient: (id, data) => authFetch(`${API_BASE}/patients/${id}`, {
    method: 'PATCH',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(r => r.json()),

  // Stats (homepage)
  getStats: () => fetch(`${API_BASE}/stats`).then(r => r.json()),
  
  // Blog
  getPosts: (page = 1, limit = 9) => fetch(`${API_BASE}/blog/?page=${page}&limit=${limit}`).then(r => r.json()),
  
  getPost: (slug) => fetch(`${API_BASE}/blog/${slug}`).then(r => r.json()),
  
  createPost: (data) => authFetch(`${API_BASE}/blog/`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(r => r.json()),
  
  updatePost: (id, data) => authFetch(`${API_BASE}/blog/${id}`, {
    method: 'PATCH',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(r => r.json()),
  
  deletePost: (id) => authFetch(`${API_BASE}/blog/${id}`, {
    method: 'DELETE'
  }).then(r => r.json()),

  // Gallery
  getGallery: () => fetch(`${API_BASE}/gallery/`).then(r => r.json()),
  
  uploadImage: (formData) => authFetch(`${API_BASE}/gallery/upload`, {
    method: 'POST',
    body: formData
  }).then(r => r.json()),
  
  deleteImage: (id) => authFetch(`${API_BASE}/gallery/${id}`, {
    method: 'DELETE'
  }).then(r => r.json()),

  // Team
  getTeam: () => fetch(`${API_BASE}/team/`).then(r => r.json()),
  
  createTeamMember: (data) => authFetch(`${API_BASE}/team/`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(r => r.json()),
  
  updateTeamMember: (id, data) => authFetch(`${API_BASE}/team/${id}`, {
    method: 'PATCH',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(r => r.json()),
  
  deleteTeamMember: (id) => authFetch(`${API_BASE}/team/${id}`, {
    method: 'DELETE'
  }).then(r => r.json()),

  // Settings
  getSettings: () => authFetch(`${API_BASE}/settings/`).then(r => r.json()),
  
  updateSettings: (data) => authFetch(`${API_BASE}/settings/`, {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(r => r.json()),
};

// Authenticated fetch helper
function authFetch(url, options = {}) {
  const token = localStorage.getItem('hrc_token');
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}` 
    }
  });
}

// Make available globally
window.api = api;
window.authFetch = authFetch;
