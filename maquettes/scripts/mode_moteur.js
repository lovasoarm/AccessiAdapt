"use strict";

const ACTIONS = [
  "Lire un message",
  "Écrire un message",
  "Paramètres",
  "Quitter",
];
let scanIndex = 0;
let scanTimer = null;
let scanSpeed = 1500;
let isPaused = false;

function init() {
  renderList();
  updateSpeedLabel();
  startScan();

  document.getElementById("speed-input").addEventListener("input", function () {
    scanSpeed = 2600 - this.value * 400;
    updateSpeedLabel();
    restartScan();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === " " || e.key === "Enter") {
      e.preventDefault();
      validate();
    }
  });
}

function renderList() {
  const list = document.getElementById("action-list");
  list.innerHTML = "";
  ACTIONS.forEach((label, i) => {
    const item = document.createElement("div");
    item.className = "action-item";
    item.id = "item-" + i;
    item.innerHTML =
      '<span class="action-label">' +
      label +
      "</span>" +
      '<svg class="action-arrow" viewBox="0 0 20 20">' +
      '<path d="M5 10h10M11 6l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/>' +
      "</svg>";
    list.appendChild(item);
  });
}

function startScan() {
  scanTimer = setInterval(advanceScan, scanSpeed);
  highlightCurrent();
}

function restartScan() {
  clearInterval(scanTimer);
  startScan();
}

function advanceScan() {
  scanIndex = (scanIndex + 1) % ACTIONS.length;
  highlightCurrent();
}

function highlightCurrent() {
  document.querySelectorAll(".action-item").forEach((el, i) => {
    el.classList.toggle("scanning", i === scanIndex);
  });
  document.getElementById("scan-label").textContent = ACTIONS[scanIndex];
}

function validate() {
  const selected = ACTIONS[scanIndex];
  clearInterval(scanTimer);

  const fb = document.getElementById("feedback");
  fb.textContent = selected + " — sélectionné";
  fb.style.display = "block";

  setTimeout(() => {
    fb.style.display = "none";
    startScan();
  }, 2000);
}

function updateSpeedLabel() {
  const val = document.getElementById("speed-input").value;
  const labels = ["Très lente", "Lente", "Normale", "Rapide", "Très rapide"];
  document.getElementById("speed-label").textContent =
    labels[val - 1] || "Normale";
}

document.addEventListener("DOMContentLoaded", init);
