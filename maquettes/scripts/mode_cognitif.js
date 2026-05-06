"use strict";

const ACTIONS = [
  {
    label: "Lire",
    guide:
      "Tu vas voir tes messages reçus. Une liste simple, un message à la fois.",
  },
  {
    label: "Écrire",
    guide: "Tu vas écrire un message. On t'aide étape par étape.",
  },
  {
    label: "Paramètres",
    guide: "Tu peux changer ton profil ou la vitesse de l'interface.",
  },
  {
    label: "Quitter",
    guide: "L'application va se fermer. Tes données sont sauvegardées.",
  },
];

const totalSteps = ACTIONS.length;

function init() {
  renderList();
  renderSteps();
  updateGuide(-1);
}

function renderList() {
  const list = document.getElementById("action-list");
  list.innerHTML = "";

  const icons = [
    '<path d="M4 6h12M4 10h8M4 14h10" stroke-linecap="round"/>',
    '<path d="M4 6h12v10H4zM8 6V4h4v2" stroke-linecap="round" stroke-linejoin="round"/>',
    '<circle cx="10" cy="10" r="7"/><path d="M10 7v3l2 2" stroke-linecap="round"/>',
    '<path d="M6 6l8 8M14 6l-8 8" stroke-linecap="round"/>',
  ];

  ACTIONS.forEach((action, i) => {
    const item = document.createElement("div");
    item.className = "action-item";
    item.tabIndex = 0;
    item.setAttribute("role", "button");
    item.innerHTML =
      '<div class="action-pic"><svg viewBox="0 0 20 20">' +
      icons[i] +
      "</svg></div>" +
      '<span class="action-label">' +
      action.label +
      "</span>" +
      '<svg class="action-arrow" viewBox="0 0 20 20">' +
      '<path d="M5 10h10M11 6l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/>' +
      "</svg>";

    item.addEventListener("click", () => {
      setClicked(item);
      selectAction(i);
    });
    item.addEventListener("focus", () => updateGuide(i));
    item.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        setClicked(item);
        selectAction(i);
      }
    });

    list.appendChild(item);
  });
}

function setClicked(el) {
  document
    .querySelectorAll(".action-item")
    .forEach((item) => item.classList.remove("clicked"));
  el.classList.add("clicked");
}

function renderSteps() {
  const dots = document.getElementById("step-dots");
  dots.innerHTML = "";
  ACTIONS.forEach((_, i) => {
    const dot = document.createElement("div");
    dot.className = "step-dot" + (i === 0 ? " active" : "");
    dot.id = "dot-" + i;
    dots.appendChild(dot);
  });
}

function updateGuide(i) {
  const box = document.getElementById("guide-text");
  if (i === -1) {
    box.textContent =
      "Choisis une action. Prends ton temps — il n'y a pas d'urgence.";
    return;
  }
  box.textContent = ACTIONS[i].guide;
  document
    .querySelectorAll(".step-dot")
    .forEach((d, idx) => d.classList.toggle("active", idx === i));
  document.getElementById("step-label").textContent =
    "Étape " + (i + 1) + " sur " + totalSteps;
}

function selectAction(i) {
  const fb = document.getElementById("feedback");
  fb.textContent = ACTIONS[i].label + " — c'est parti.";
  fb.style.display = "block";
  updateGuide(i);
  setTimeout(() => {
    fb.style.display = "none";
  }, 2500);
}

document.addEventListener("DOMContentLoaded", init);
