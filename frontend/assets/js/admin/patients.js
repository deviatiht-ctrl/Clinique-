/* Admin Patients Module - Haiti Reh-Care */

document.addEventListener('DOMContentLoaded', async () => {
  // Load patients data
  await loadPatients();
});

async function loadPatients() {
  try {
    // In a real app, fetch from API
    // const patients = await api.getPatients();
    
    // Mock data for demo
    const patients = [
      {
        id: 1,
        patient_code: "P20240101001",
        full_name: "Jean Baptiste",
        phone: "+509 3644-0001",
        primary_condition: "Amputation tibiale",
        economic_status: "reduced",
        created_at: "2024-01-15T10:30:00"
      },
      {
        id: 2,
        patient_code: "P20240102002",
        full_name: "Marie Joseph",
        phone: "+509 3644-0002",
        primary_condition: "Scoliose",
        economic_status: "normal",
        created_at: "2024-01-20T14:15:00"
      },
      {
        id: 3,
        patient_code: "P20240103003",
        full_name: "Pierre Louis",
        phone: "+509 3644-0003",
        primary_condition: "Prothèse fémorale",
        economic_status: "very_limited",
        created_at: "2024-02-01T09:00:00"
      }
    ];
    
    const tbody = document.getElementById('patientsTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = patients.map(p => `
      <tr>
        <td>${p.patient_code}</td>
        <td>${p.full_name}</td>
        <td>${p.primary_condition || '-'}</td>
        <td>${p.phone}</td>
        <td>${formatDate(p.created_at)}</td>
        <td>
          <span class="pill ${p.economic_status === 'very_limited' ? 'pill-green' : 'pill-gray'}">
            ${formatEconomicStatus(p.economic_status)}
          </span>
        </td>
        <td>
          <div class="table-actions-cell">
            <button class="action-btn" onclick="viewPatient(${p.id})" title="Voir">
              <i data-lucide="eye"></i>
            </button>
            <button class="action-btn edit" onclick="editPatient(${p.id})" title="Modifier">
              <i data-lucide="edit"></i>
            </button>
          </div>
        </td>
      </tr>
    `).join('');
    
    lucide.createIcons();
  } catch (error) {
    console.error('Failed to load patients:', error);
  }
}

function formatDate(dateString) {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString('fr-FR');
}

function formatEconomicStatus(status) {
  const labels = {
    'normal': 'Normal',
    'reduced': 'Réduit',
    'very_limited': 'Très limité'
  };
  return labels[status] || status;
}

function viewPatient(id) {
  // Open side panel with patient details
  alert('Détails du patient ' + id + ' - Fonctionnalité à implémenter');
}

function editPatient(id) {
  // Open side panel with patient edit form
  alert('Modifier le patient ' + id + ' - Fonctionnalité à implémenter');
}

// Search functionality
const searchInput = document.getElementById('searchPatients');
if (searchInput) {
  searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const rows = document.querySelectorAll('#patientsTableBody tr');
    
    rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
  });
}
