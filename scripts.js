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
  const nbEtoiles = window.innerWidth < 768 ? 300 : 800;

  const etoiles = Array.from({ length: nbEtoiles }, () => ({
    x:       Math.random() * canvas.width,
    y:       Math.random() * canvas.height,
    taille:  Math.random() * 1 + 0.5,
    opacite: Math.random(),
    delta:   Math.random() * 0.01 + 0.01  
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

//ROtation des cartes au click
document.querySelectorAll('.formation-carte').forEach(carte => {
  carte.addEventListener('click' , () => {
    carte.classList.toggle('retournee');
  });
});

// ==========================================
// CHATBOT WIDGET
// ==========================================
const chatToggleBtn  = document.getElementById("chat-toggle-btn");
const chatWindow     = document.getElementById("chat-window");
const chatCloseBtn   = document.getElementById("chat-close-btn");
const chatInput      = document.getElementById("chat-input");
const chatSendBtn    = document.getElementById("chat-send-btn");
const chatMessages   = document.getElementById("chat-messages");
const chatTyping     = document.getElementById("chat-typing");
const chatIconOpen   = document.getElementById("chat-icon-open");
const chatIconClose  = document.getElementById("chat-icon-close");

// --- URL de API FastAPI
const API_URL = "https://portofolio-tw1d.onrender.com";

// --- Ouvrir / Fermer la fenêtre du chat
function toggleChat() {
  const isOpen = chatWindow.classList.contains("chat-open");
  chatWindow.classList.toggle("chat-open");
  chatWindow.setAttribute("aria-hidden", isOpen ? "true" : "false");
  chatIconOpen.style.display  = isOpen ? "block" : "none";
  chatIconClose.style.display = isOpen ? "none"  : "block";
  if (!isOpen) chatInput.focus();
}
chatToggleBtn.addEventListener("click", toggleChat);
chatCloseBtn.addEventListener("click",  toggleChat);

// --- Ajouter une bulle de message dans la fenêtre
function appendMessage(text, role) {
  const msgDiv    = document.createElement("div");
  msgDiv.className = `chat-msg ${role}`; // "bot" ou "user"

  const bubble    = document.createElement("div");
  bubble.className = "chat-bubble";
  bubble.textContent = text;

  msgDiv.appendChild(bubble);
  chatMessages.appendChild(msgDiv);

  // Scroll automatique vers le bas
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// --- Envoyer une question à l'API
async function sendMessage() {
  const question = chatInput.value.trim();
  if (!question) return;

  // Afficher la question de l'utilisateur
  appendMessage(question, "user");
  chatInput.value = "";

  // Afficher l'indicateur de frappe (⋯)
  chatTyping.style.display = "block";
  chatMessages.scrollTop = chatMessages.scrollHeight;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question }),
    });

    if (!response.ok) throw new Error("Erreur serveur : " + response.status);

    const data = await response.json();
    chatTyping.style.display = "none";
    appendMessage(data.answer, "bot");

  } catch (error) {
    chatTyping.style.display = "none";
    appendMessage("⚠️ Sorry, I'm having trouble connecting to the server. Please try again later.", "bot");
    console.error("Chatbot error:", error);
  }
}

// --- Déclencheurs d'envoi (bouton + touche Entrée)
chatSendBtn.addEventListener("click", sendMessage);
chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});