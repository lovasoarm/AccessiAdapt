"use strict";

const PROFILES = {
  visuel: {
    label: "Handicap visuel",
    color: "#c05a1f",
    tags: [
      "Grand texte",
      "Contraste fort",
      "Synthèse vocale",
      "Navigation clavier",
    ],
    img: "https://images.unsplash.com/photo-1516585427167-9f4af9627e6c?w=400&q=80",
    imgAlt: "Personne utilisant un lecteur d'écran devant un ordinateur",
    adaptations: "Police 22px · Contraste noir/blanc · TTS activé",
  },
  moteur: {
    label: "Handicap moteur",
    color: "#1a6b3a",
    tags: ["Gros boutons", "Mono-bouton", "Balayage auto", "Anti-double-clic"],
    img: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&q=80",
    imgAlt: "Mains utilisant un clavier adapté",
    adaptations: "Boutons larges · Balayage 1.5s · 1 seul bouton",
  },
  auditif: {
    label: "Handicap auditif",
    color: "#1a4a7a",
    tags: ["Sous-titres", "Alertes visuelles", "Vibration", "Transcription"],
    img: "https://images.unsplash.com/photo-1588776814546-1ffbb3f7e8a5?w=400&q=80",
    imgAlt: "Interface avec sous-titres et notifications visuelles",
    adaptations: "Sous-titres · 0 dépendance audio · Alertes visuelles",
  },
  cognitif: {
    label: "Handicap cognitif",
    color: "#6b2a7a",
    tags: [
      "Interface simple",
      "Guidage pas à pas",
      "Pictogrammes",
      "1 tâche/écran",
    ],
    img: "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=400&q=80",
    imgAlt: "Personne utilisant une interface épurée et simple",
    adaptations: "Interface simplifiée · Navigation linéaire · Pictogrammes",
  },
};

const selected = new Set();

const $ = (id) => document.getElementById(id);
const $$ = (sel) => document.querySelectorAll(sel);

function toggleProfile(key) {
  if (selected.has("standard")) {
    $("card-standard").classList.remove("selected");
    selected.delete("standard");
  }

  const card = $("card-" + key);
  if (selected.has(key)) {
    selected.delete(key);
    card.classList.remove("selected");
  } else {
    selected.add(key);
    card.classList.add("selected");
  }
  updateFooter();
}

function toggleStandard() {
  selected.clear();
  $$(".profile-card").forEach((c) => c.classList.remove("selected"));

  const card = $("card-standard");
  if (card.classList.contains("selected")) {
    card.classList.remove("selected");
  } else {
    card.classList.add("selected");
    selected.add("standard");
  }
  updateFooter();
}

function updateFooter() {
  const btn = $("btn-continue");
  const hint = $("hint-text");
  const count = selected.size;

  if (count === 0) {
    btn.disabled = true;
    hint.innerHTML = "Sélectionne au moins un profil pour continuer.";
    return;
  }

  btn.disabled = false;

  if (selected.has("standard")) {
    hint.innerHTML = "<strong>Mode standard</strong> — configuration manuelle.";
    return;
  }

  const labels = [...selected].map((k) => PROFILES[k].label);

  if (count === 1) {
    hint.innerHTML = `<strong>${labels[0]}</strong> sélectionné.`;
  } else {
    hint.innerHTML = `<strong>Profil combiné</strong> — ${labels.join(" + ")}.`;
  }
}

function goToConfirm() {
  const container = $("recap-items");
  container.innerHTML = "";

  selected.forEach((key) => {
    const p =
      key === "standard"
        ? {
            label: "Standard / Personnalisé",
            color: "#3a3a3a",
            tags: ["Configuration manuelle"],
            img: "",
            adaptations: "Tous les paramètres accessibles manuellement",
          }
        : PROFILES[key];

    const item = document.createElement("div");
    item.className = "recap-item";
    item.innerHTML = `
      <div class="recap-color" style="background:${p.color}"></div>
      ${p.img ? `<img class="recap-item-img" src="${p.img}" alt="${p.imgAlt || ""}" loading="lazy">` : ""}
      <div class="recap-item-info">
        <div class="recap-item-title">${p.label}</div>
        <div class="recap-item-tags">${p.adaptations}</div>
      </div>
    `;
    container.appendChild(item);
  });

  let msg = "";
  if (selected.has("standard")) {
    msg =
      "Interface en mode standard — tu configures chaque paramètre toi-même.";
  } else if (selected.size > 1) {
    msg =
      "Profil combiné détecté. Les adaptations compatibles seront toutes activées automatiquement.";
  } else {
    const key = [...selected][0];
    const data = PROFILES[key];
    msg = `Mode ${data.label.toLowerCase()} activé. L'interface s'adapte automatiquement à tes besoins.`;
  }
  $("confirm-sub").textContent = msg;

  $("screen-select").style.display = "none";
  $("screen-confirm").style.display = "block";
  $("screen-confirm").style.animation = "none";
  void $("screen-confirm").offsetWidth;
  $("screen-confirm").style.animation = "fadeUp .4s ease both";

  window.scrollTo({ top: 0, behavior: "smooth" });
}

function goBack() {
  $("screen-confirm").style.display = "none";
  $("screen-select").style.display = "block";
}

function launchApp() {
  const profil = [...selected].join("+");
  alert(
    `Lancement avec le profil : ${profil}\n\nProchaine page → mode_standard.html`,
  );
}

document.addEventListener("DOMContentLoaded", () => {
  updateFooter();
});
