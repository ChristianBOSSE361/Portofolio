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


// Génération des étoiles
document.querySelectorAll(".etoiles-bg").forEach(container => {
  const canvas = document.createElement('canvas');
  container.appendChild(canvas);

  canvas.style.cssText = `
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
  `;

  // Taille réelle en pixels du conteneur
  canvas.width  = container.offsetWidth;
  canvas.height = container.offsetHeight;

  const ctx = canvas.getContext('2d');
  const nbEtoiles = window.innerWidth < 768 ? 300 : 1000;

  const etoiles = Array.from({ length: nbEtoiles }, () => ({
    x:       Math.random() * canvas.width,
    y:       Math.random() * canvas.height,
    taille:  Math.random() * 2 + 0.5,
    opacite: Math.random(),
    delta:   Math.random() * 0.01 + 0.01  // scintillement plus doux
  }));

  function animer() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    etoiles.forEach(e => {
      e.opacite += e.delta;
      if (e.opacite >= 1 || e.opacite <= 0) e.delta *= -1;

      ctx.beginPath();
      ctx.arc(e.x, e.y, e.taille, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${e.opacite.toFixed(2)})`;
      ctx.fill();
    });

    requestAnimationFrame(animer);
  }

  animer();

  // Si la fenêtre est redimensionnée, le canvas se remet à jour
  window.addEventListener('resize', () => {
    canvas.width  = container.offsetWidth;
    canvas.height = container.offsetHeight;
  });
});