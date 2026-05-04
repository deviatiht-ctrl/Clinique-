/* Homepage Module - Haiti Reh-Care */

document.addEventListener('DOMContentLoaded', async () => {
  // Load stats
  try {
    const stats = await api.getStats();
    if (stats) {
      document.getElementById('statPatients').textContent = (stats.patients || 500) + '+';
      document.getElementById('statProsthetics').textContent = (stats.appointments_completed || 800) + '+';
    }
  } catch (error) {
    console.log('Stats fetch failed, using defaults');
  }
  
  // Testimonials drag scroll
  const track = document.getElementById('testimonialsTrack');
  if (track) {
    let isDown = false;
    let startX;
    let scrollLeft;
    
    track.addEventListener('mousedown', (e) => {
      isDown = true;
      track.style.cursor = 'grabbing';
      startX = e.pageX - track.offsetLeft;
      scrollLeft = track.scrollLeft;
    });
    
    track.addEventListener('mouseleave', () => {
      isDown = false;
      track.style.cursor = 'grab';
    });
    
    track.addEventListener('mouseup', () => {
      isDown = false;
      track.style.cursor = 'grab';
    });
    
    track.addEventListener('mousemove', (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - track.offsetLeft;
      const walk = (x - startX) * 2;
      track.scrollLeft = scrollLeft - walk;
    });
  }
  
  // Donation amount buttons
  const amountBtns = document.querySelectorAll('.amount-btn');
  amountBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      amountBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });
});
