/* Admin Appointments Module - Haiti Reh-Care */

document.addEventListener('DOMContentLoaded', async () => {
  // Load appointments data
  await loadAppointments();
});

async function loadAppointments() {
  try {
    // Mock data for demo
    const appointments = [
      {
        id: 1,
        booking_code: "HRC-A1B2C3",
        guest_name: "Jean Baptiste",
        guest_phone: "+509 3644-0001",
        appointment_date: "2025-01-20",
        appointment_time: "09:00",
        appointment_type: "follow_up",
        status: "confirmed"
      },
      {
        id: 2,
        booking_code: "HRC-D4E5F6",
        guest_name: "Marie Joseph",
        guest_phone: "+509 3644-0002",
        appointment_date: "2025-01-20",
        appointment_time: "10:00",
        appointment_type: "first_consultation",
        status: "confirmed"
      },
      {
        id: 3,
        booking_code: "HRC-G7H8I9",
        guest_name: "Pierre Louis",
        guest_phone: "+509 3644-0003",
        appointment_date: "2025-01-21",
        appointment_time: "11:00",
        appointment_type: "measurement",
        status: "pending"
      }
    ];
    
    const tbody = document.getElementById('appointmentsTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = appointments.map(a => `
      <tr>
        <td>${formatDate(a.appointment_date)}</td>
        <td>${a.appointment_time}</td>
        <td>${a.guest_name}</td>
        <td>${formatAppointmentType(a.appointment_type)}</td>
        <td>
          <span class="status-badge status-${a.status}">
            <i data-lucide="${getStatusIcon(a.status)}" style="width: 12px; height: 12px;"></i>
            ${formatStatus(a.status)}
          </span>
        </td>
        <td>
          <div class="table-actions-cell">
            <button class="action-btn" onclick="viewAppointment(${a.id})" title="Voir">
              <i data-lucide="eye"></i>
            </button>
            <button class="action-btn edit" onclick="confirmAppointment(${a.id})" title="Confirmer">
              <i data-lucide="check"></i>
            </button>
            <a href="https://wa.me/${a.guest_phone.replace(/\D/g, '')}" class="action-btn" target="_blank" title="WhatsApp">
              <i data-lucide="message-circle"></i>
            </a>
          </div>
        </td>
      </tr>
    `).join('');
    
    lucide.createIcons();
  } catch (error) {
    console.error('Failed to load appointments:', error);
  }
}

function formatDate(dateString) {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString('fr-FR');
}

function formatAppointmentType(type) {
  const labels = {
    'first_consultation': 'Première consultation',
    'follow_up': 'Suivi',
    'emergency': 'Urgence',
    'measurement': 'Prise de mesures',
    'device_fitting': 'Ajustement'
  };
  return labels[type] || type;
}

function formatStatus(status) {
  const labels = {
    'pending': 'En attente',
    'confirmed': 'Confirmé',
    'completed': 'Terminé',
    'cancelled': 'Annulé'
  };
  return labels[status] || status;
}

function getStatusIcon(status) {
  const icons = {
    'pending': 'clock',
    'confirmed': 'check-circle',
    'completed': 'check',
    'cancelled': 'x-circle'
  };
  return icons[status] || 'circle';
}

function viewAppointment(id) {
  alert('Détails du rendez-vous ' + id + ' - Fonctionnalité à implémenter');
}

async function confirmAppointment(id) {
  try {
    // await api.updateAppointmentStatus(id, 'confirmed');
    alert('Rendez-vous confirmé!');
    await loadAppointments(); // Refresh
  } catch (error) {
    alert('Erreur lors de la confirmation');
  }
}
