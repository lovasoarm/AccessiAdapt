"use strict";

const ACTIONS = [
  "Lire un message",
  "Écrire un message",
  "Paramètres",
  "Quitter",
];

function init() {
  const list = document.getElementById("action-list");

  ACTIONS.forEach((label, i) => {
    const item = document.createElement("div");
    item.className = "action-item";
    item.tabIndex = 0;
    item.setAttribute("role", "button");
    item.innerHTML =
      '<span class="action-label">' +
      label +
      "</span>" +
      '<svg class="action-arrow" viewBox="0 0 20 20">' +
      '<path d="M5 10h10M11 6l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/>' +
      "</svg>";

    item.addEventListener("click", () => selectAction(label));
    item.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        selectAction(label);
      }
    });

    list.appendChild(item);
  });
}

function selectAction(label) {
  if (label === "Quitter") {
    window.location.href = "../pages/index.html";
    return;
  }

  const fb = document.getElementById("feedback");
  fb.textContent = label + " — ouvert";
  fb.style.display = "block";
  setTimeout(() => {
    fb.style.display = "none";
  }, 2000);
}

document.addEventListener("DOMContentLoaded", init);
