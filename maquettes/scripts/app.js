"use strict";

const PROFILES = {
  v: {
    id: "card-v",
    name: "Visuel",
    adapt: "Police 22px · Contraste noir/blanc · Synthèse vocale",
  },
  m: {
    id: "card-m",
    name: "Moteur",
    adapt: "Boutons larges · Balayage auto · Mono-bouton",
  },
  a: {
    id: "card-a",
    name: "Auditif",
    adapt: "Sous-titres · Alertes visuelles · Zéro dépendance audio",
  },
  c: {
    id: "card-c",
    name: "Cognitif",
    adapt: "Interface simple · 1 tâche par écran · Pictogrammes",
  },
};

const selected = new Set();

function toggleProfile(key) {
  if (selected.has("s")) {
    setCard("card-std", false);
    selected.delete("s");
  }

  const isOn = selected.has(key);
  setCard(PROFILES[key].id, !isOn);

  if (isOn) selected.delete(key);
  else selected.add(key);

  updateFooter();
}

function toggleStandard() {
  selected.clear();
  Object.values(PROFILES).forEach((p) => setCard(p.id, false));

  const wasOn = document.getElementById("card-std").classList.contains("on");
  setCard("card-std", !wasOn);

  if (!wasOn) selected.add("s");
  updateFooter();
}

function setCard(id, on) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.toggle("on", on);
  el.setAttribute("aria-checked", String(on));
}

function updateFooter() {
  const btn = document.getElementById("btn-continue");
  const hint = document.getElementById("hint");

  if (selected.size === 0) {
    btn.disabled = true;
    hint.innerHTML = "Sélectionne au moins un profil pour continuer.";
    return;
  }

  btn.disabled = false;

  if (selected.has("s")) {
    hint.innerHTML = "<b>Mode standard</b> sélectionné.";
    return;
  }

  const names = [...selected].map((k) => PROFILES[k].name);

  if (names.length === 1) {
    hint.innerHTML = "<b>Profil " + names[0] + "</b> sélectionné.";
  } else {
    hint.innerHTML = "<b>Profil combiné</b> — " + names.join(" + ") + ".";
  }
}

function goConfirm() {
  const list = document.getElementById("recap-list");
  list.innerHTML = "";

  selected.forEach((k) => {
    const p =
      k === "s"
        ? {
            name: "Standard / Personnalisé",
            adapt: "Configuration manuelle complète",
          }
        : PROFILES[k];

    const row = document.createElement("div");
    row.className = "recap-row";
    row.innerHTML =
      '<div class="recap-bar"></div>' +
      "<div>" +
      '<div class="recap-name">' +
      p.name +
      "</div>" +
      '<div class="recap-adapt">' +
      p.adapt +
      "</div>" +
      "</div>";
    list.appendChild(row);
  });

  const sub = document.getElementById("cf-sub");
  if (selected.has("s")) {
    sub.textContent = "Tous les paramètres sont accessibles manuellement.";
  } else if (selected.size > 1) {
    sub.textContent =
      "Profil combiné — toutes les adaptations compatibles sont activées.";
  } else {
    const name = PROFILES[[...selected][0]].name;
    sub.textContent =
      "Mode " + name + " activé — interface adaptée automatiquement.";
  }

  showScreen("screen-confirm");
}

function goBack() {
  showScreen("screen-select");
}

function launchApp() {
  const profil = [...selected]
    .map((k) => (k === "s" ? "standard" : PROFILES[k].name.toLowerCase()))
    .join("+");

  window.location.href = "mode_standard.html";
}

function showScreen(id) {
  document
    .querySelectorAll(".screen")
    .forEach((s) => s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

document.addEventListener("DOMContentLoaded", updateFooter);
