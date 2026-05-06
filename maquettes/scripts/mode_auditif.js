"use strict";

const ACTIONS = [
  {
    label: "Lire un message",
    subtitle: "Ouvre la liste de tes messages reçus.",
  },
  {
    label: "Écrire un message",
    subtitle: "Compose et envoie un nouveau message.",
  },
  { label: "Paramètres", subtitle: "Modifie ton profil et tes préférences." },
  { label: "Quitter", subtitle: "Ferme l'application AccessiAdapt." },
];

let notifTimer = null;

function init() {
  renderList();
}

function renderList() {
  const list = document.getElementById("action-list");
  list.innerHTML = "";

  ACTIONS.forEach((action, i) => {
    const item = document.createElement("div");
    item.className = "action-item";
    item.tabIndex = 0;
    item.setAttribute("role", "button");
    item.innerHTML =
      '<span class="action-label">' +
      action.label +
      "</span>" +
      '<svg class="action-arrow" viewBox="0 0 20 20">' +
      '<path d="M5 10h10M11 6l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/>' +
      "</svg>";

    item.addEventListener("click", () => selectAction(i));
    item.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        selectAction(i);
      }
    });
    item.addEventListener("focus", () => showSubtitle(i));

    list.appendChild(item);
  });
}

function selectAction(i) {
  showNotif(ACTIONS[i].label + " — ouvert");
  showSubtitle(i);
}

function showNotif(text) {
  const notif = document.getElementById("notif");
  const label = document.getElementById("notif-label");

  label.textContent = text;
  notif.classList.add("visible");

  clearTimeout(notifTimer);
  notifTimer = setTimeout(() => notif.classList.remove("visible"), 3000);
}

function showSubtitle(i) {
  document.getElementById("subtitles-text").textContent = ACTIONS[i].subtitle;
}

document.addEventListener("DOMContentLoaded", init);
