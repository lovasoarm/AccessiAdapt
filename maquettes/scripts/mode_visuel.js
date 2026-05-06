"use strict";

const ACTIONS = [
  "Lire un message",
  "Écrire un message",
  "Paramètres",
  "Quitter",
];
let focusIndex = 0;

function init() {
  renderList();
  setFocus(0);
  speak(ACTIONS[0]);
}

function renderList() {
  const list = document.getElementById("action-list");
  list.innerHTML = "";

  ACTIONS.forEach((label, i) => {
    const item = document.createElement("div");
    item.className = "action-item";
    item.id = "item-" + i;
    item.tabIndex = 0;
    item.setAttribute("role", "button");
    item.innerHTML =
      '<span class="action-label">' +
      label +
      "</span>" +
      '<svg class="action-arrow" viewBox="0 0 20 20">' +
      '<path d="M5 10h10M11 6l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/>' +
      "</svg>";

    item.addEventListener("click", () => selectAction(i));
    item.addEventListener("focus", () => setFocus(i));
    item.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        moveFocus(1);
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        moveFocus(-1);
      }
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        selectAction(i);
      }
    });

    list.appendChild(item);
  });
}

function setFocus(i) {
  focusIndex = i;
  document.querySelectorAll(".action-item").forEach((el, idx) => {
    el.classList.toggle("focused", idx === i);
  });
  document.getElementById("focus-label").textContent = ACTIONS[i];
  speak(ACTIONS[i]);
}

function moveFocus(dir) {
  const next = (focusIndex + dir + ACTIONS.length) % ACTIONS.length;
  setFocus(next);
  document.getElementById("item-" + next).focus();
}

function selectAction(i) {
  speak(ACTIONS[i] + " — ouvert");
  document.getElementById("feedback").textContent = ACTIONS[i] + " — ouvert";
  document.getElementById("feedback").style.display = "block";
  setTimeout(() => {
    document.getElementById("feedback").style.display = "none";
  }, 2500);
}

function speak(text) {
  document.getElementById("tts-text").textContent = '"' + text + '"';
}

document.addEventListener("DOMContentLoaded", init);
