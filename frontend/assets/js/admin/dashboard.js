/* Admin Dashboard Module - Haiti Reh-Care */

document.addEventListener('DOMContentLoaded', async () => {
  // Load dashboard data
  await loadDashboardData();
});

async function loadDashboardData() {
  try {
    // In a real app, fetch from API
    // const data = await api.getDashboardStats();
    
    // Mock data for demo
    const data = {
      todayAppointments: 4,
      newPatients: 12,
      totalPatients: 156,
      pendingAppointments: 3
    };
    
    // Update KPI cards
    document.getElementById('todayAppointments').textContent = data.todayAppointments;
    document.getElementById('newPatients').textContent = data.newPatients;
    document.getElementById('totalPatients').textContent = data.totalPatients;
    document.getElementById('pendingAppointments').textContent = data.pendingAppointments;
    
    // Update badges
    document.getElementById('pendingBadge').textContent = data.pendingAppointments;
    
  } catch (error) {
    console.error('Failed to load dashboard data:', error);
  }
}
