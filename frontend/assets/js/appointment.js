/* Appointment Booking Module - Haiti Reh-Care */

let currentStep = 1;
const totalSteps = 4;
let selectedDate = null;
let selectedTime = null;
let selectedType = null;

document.addEventListener('DOMContentLoaded', () => {
  // Initialize appointment type cards
  const typeCards = document.querySelectorAll('.appointment-type-card');
  typeCards.forEach(card => {
    card.addEventListener('click', () => {
      typeCards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      selectedType = card.dataset.type;
      document.getElementById('appointmentType').value = selectedType;
      document.getElementById('typeError').style.display = 'none';
    });
  });
  
  // Initialize calendar
  initCalendar();
  
  // Navigation buttons
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  
  prevBtn?.addEventListener('click', () => {
    if (currentStep > 1) {
      goToStep(currentStep - 1);
    }
  });
  
  nextBtn?.addEventListener('click', async () => {
    if (await validateStep(currentStep)) {
      if (currentStep < totalSteps) {
        goToStep(currentStep + 1);
      } else {
        submitAppointment();
      }
    }
  });
});

function goToStep(step) {
  // Hide current step
  document.querySelector(`.step-panel[data-step="${currentStep}"]`).classList.remove('active');
  
  // Show new step
  document.querySelector(`.step-panel[data-step="${step}"]`).classList.add('active');
  
  // Update step indicator
  document.querySelectorAll('.step-dot').forEach((dot, index) => {
    const dotStep = index + 1;
    if (dotStep < step) {
      dot.classList.add('completed');
      dot.classList.remove('active');
      dot.innerHTML = '<i data-lucide="check" style="width: 16px; height: 16px;"></i>';
    } else if (dotStep === step) {
      dot.classList.add('active');
      dot.classList.remove('completed');
      dot.textContent = dotStep;
    } else {
      dot.classList.remove('active', 'completed');
      dot.textContent = dotStep;
    }
  });
  
  // Update step lines
  document.querySelectorAll('.step-line').forEach((line, index) => {
    if (index < step - 1) {
      line.classList.add('completed');
    } else {
      line.classList.remove('completed');
    }
  });
  
  // Update buttons
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  
  prevBtn.style.display = step === 1 ? 'none' : 'block';
  nextBtn.innerHTML = step === totalSteps ? '<i data-lucide="check"></i> Confirmer' : 'Continuer';
  
  // Update summary if going to step 4
  if (step === 4) {
    updateSummary();
  }
  
  // Re-initialize Lucide icons
  lucide.createIcons();
  
  currentStep = step;
}

async function validateStep(step) {
  switch (step) {
    case 1:
      if (!selectedType) {
        document.getElementById('typeError').style.display = 'flex';
        return false;
      }
      return true;
      
    case 2:
      if (!selectedDate || !selectedTime) {
        document.getElementById('dateTimeError').style.display = 'flex';
        return false;
      }
      return true;
      
    case 3:
      const form = document.getElementById('appointmentForm');
      const required = form.querySelectorAll('[required]');
      let valid = true;
      
      required.forEach(field => {
        if (!field.value) {
          field.classList.add('error');
          valid = false;
        } else {
          field.classList.remove('error');
        }
      });
      
      return valid;
      
    default:
      return true;
  }
}

function updateSummary() {
  const typeLabels = {
    'first_consultation': 'Première consultation',
    'follow_up': 'Suivi',
    'emergency': 'Urgence',
    'measurement': 'Prise de mesures'
  };
  
  document.getElementById('summaryType').textContent = typeLabels[selectedType] || selectedType;
  document.getElementById('summaryDate').textContent = selectedDate ? new Date(selectedDate).toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' }) : '-';
  document.getElementById('summaryTime').textContent = selectedTime || '-';
  document.getElementById('summaryName').textContent = document.querySelector('input[name="first_name"]')?.value + ' ' + document.querySelector('input[name="last_name"]')?.value || '-';
  document.getElementById('summaryPhone').textContent = document.querySelector('input[name="phone"]')?.value || '-';
}

async function submitAppointment() {
  const form = document.getElementById('appointmentForm');
  const formData = new FormData(form);
  
  const data = {
    appointment_type: selectedType,
    appointment_date: selectedDate,
    appointment_time: selectedTime,
    guest_name: formData.get('first_name') + ' ' + formData.get('last_name'),
    guest_phone: formData.get('phone'),
    guest_email: formData.get('email'),
    guest_condition: formData.get('condition'),
    notes: formData.get('message')
  };
  
  try {
    const result = await api.createAppointment(data);
    
    if (result.booking_code) {
      // Show success
      document.querySelector(`.step-panel[data-step="${currentStep}"]`).classList.remove('active');
      document.querySelector('.step-panel[data-step="success"]').classList.add('active');
      document.getElementById('confirmationNumber').textContent = result.booking_code;
      document.getElementById('formNavigation').style.display = 'none';
      lucide.createIcons();
    } else {
      showToast('Erreur lors de la création du rendez-vous. Veuillez réessayer.', 'error');
    }
  } catch (error) {
    showToast('Erreur de connexion. Veuillez réessayer.', 'error');
  }
}

// Calendar functions
let currentMonth = new Date();

function initCalendar() {
  renderCalendar(currentMonth);
  
  document.getElementById('prevMonth')?.addEventListener('click', () => {
    currentMonth.setMonth(currentMonth.getMonth() - 1);
    renderCalendar(currentMonth);
  });
  
  document.getElementById('nextMonth')?.addEventListener('click', () => {
    currentMonth.setMonth(currentMonth.getMonth() + 1);
    renderCalendar(currentMonth);
  });
}

function renderCalendar(date) {
  const year = date.getFullYear();
  const month = date.getMonth();
  
  // Update title
  const monthNames = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'];
  document.getElementById('calendarMonth').textContent = `${monthNames[month]} ${year}`;
  
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const daysInMonth = lastDay.getDate();
  const startDayOfWeek = firstDay.getDay();
  
  const grid = document.getElementById('calendarGrid');
  grid.innerHTML = '';
  
  // Weekday headers
  const weekdays = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];
  weekdays.forEach(day => {
    const el = document.createElement('div');
    el.className = 'calendar-weekday';
    el.textContent = day;
    grid.appendChild(el);
  });
  
  // Empty cells before first day
  for (let i = 0; i < startDayOfWeek; i++) {
    const el = document.createElement('div');
    grid.appendChild(el);
  }
  
  // Days
  const today = new Date();
  for (let day = 1; day <= daysInMonth; day++) {
    const el = document.createElement('div');
    el.className = 'calendar-day';
    el.textContent = day;
    
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    
    // Check if past date
    const currentDate = new Date(year, month, day);
    if (currentDate < new Date(today.setHours(0, 0, 0, 0))) {
      el.classList.add('disabled');
    } else {
      el.addEventListener('click', () => selectDate(dateStr, el));
    }
    
    // Check if today
    if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
      el.classList.add('today');
    }
    
    // Check if selected
    if (selectedDate === dateStr) {
      el.classList.add('selected');
    }
    
    grid.appendChild(el);
  }
}

async function selectDate(date, element) {
  // Remove previous selection
  document.querySelectorAll('.calendar-day').forEach(el => el.classList.remove('selected'));
  
  // Add selection
  element.classList.add('selected');
  selectedDate = date;
  document.getElementById('selectedDate').value = date;
  document.getElementById('dateTimeError').style.display = 'none';
  
  // Show time slots container
  document.getElementById('timeSlotsContainer').style.display = 'block';
  
  // Load time slots
  await loadTimeSlots(date);
}

async function loadTimeSlots(date) {
  const container = document.getElementById('timeSlots');
  container.innerHTML = '<p>Chargement...</p>';
  
  try {
    // In a real app, this would fetch from the backend
    // const slots = await api.getSlots(date);
    
    // Mock slots for demo
    const allSlots = ['08:00', '09:00', '10:00', '11:00', '13:00', '14:00'];
    const bookedSlots = ['09:00', '14:00']; // Mock booked slots
    
    container.innerHTML = '';
    
    allSlots.forEach(slot => {
      const el = document.createElement('button');
      el.type = 'button';
      el.className = 'time-slot';
      el.textContent = slot;
      
      if (bookedSlots.includes(slot)) {
        el.classList.add('disabled');
        el.disabled = true;
      } else {
        el.addEventListener('click', () => selectTime(slot, el));
      }
      
      if (selectedTime === slot) {
        el.classList.add('selected');
      }
      
      container.appendChild(el);
    });
  } catch (error) {
    container.innerHTML = '<p class="form-error">Erreur de chargement des créneaux</p>';
  }
}

function selectTime(time, element) {
  // Remove previous selection
  document.querySelectorAll('.time-slot').forEach(el => el.classList.remove('selected'));
  
  // Add selection
  element.classList.add('selected');
  selectedTime = time;
  document.getElementById('selectedTime').value = time;
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <i data-lucide="${type === 'error' ? 'alert-circle' : 'info'}"></i>
    <span>${message}</span>
  `;
  container.appendChild(toast);
  lucide.createIcons();
  
  setTimeout(() => {
    toast.remove();
  }, 4000);
}
