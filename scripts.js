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
const nbEtoiles = window.innerWidth < 768 ? 300 : 1000;

document.querySelectorAll(".etoiles-bg").forEach(container => {  // sécurité : on vérifie que l'élément existe
  for (let i = 0; i < nbEtoiles; i++) {
    const etoile = document.createElement('div');
    etoile.classList.add('etoile');
    // Taille aléatoire entre 0.5 et 2.5px
    const taille = Math.random() * 2 + 0.5;
    // Durée d'animation aléatoire entre 1.5s et 4.5s
    const duree  = (Math.random() * 3 + 1.5).toFixed(1);
    // Délai aléatoire pour que les étoiles ne scintillent pas toutes en même temps
    const delai  = (Math.random() * 4).toFixed(1);
    etoile.style.cssText = `
      width:            ${taille}px;
      height:           ${taille}px;
      top:              ${Math.random() * 100}%;
      left:             ${Math.random() * 100}%;
      --d:              ${duree}s;
      animation-delay:  ${delai}s;
      opacity:          ${(Math.random() * 0.5 + 0.2).toFixed(2)};
    `;
    container.appendChild(etoile);
  }
});