const navbar     = document.getElementById('navbar');
const hamburger  = document.getElementById('hamburger');
const navLiens   = document.querySelector('.nav-liens');
// 1. Fond blanc quand on scroll vers le bas
window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});
// 2. Ouvrir / fermer le menu hamburger
hamburger.addEventListener('click', () => {
  navLiens.classList.toggle('ouvert');
});
// 3. Fermer le menu quand on clique sur un lien
navLiens.querySelectorAll('a').forEach(lien => {
  lien.addEventListener('click', () => {
    navLiens.classList.remove('ouvert');
  });
});

const cards = document.querySelectorAll(".planet-card");

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
    }
  });
}, {
  threshold: 0.2
});

cards.forEach(card => observer.observe(card));