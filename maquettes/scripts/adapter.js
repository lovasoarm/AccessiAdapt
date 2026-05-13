function getProfiles() {
  const params = new URLSearchParams(window.location.search);
  const raw = params.get("profiles") || "";
  return new Set(raw.split(",").filter(Boolean));
}

function buildConfig(profiles) {
  const config = {
    fontSize: "normal",
    contrast: false,
    tts: false,
    captions: false,
    largeButtons: false,
    singleSwitch: false,
    simplified: false,
  };

  if (profiles.has("v")) {
    config.contrast = true;
    config.tts = true;
    config.fontSize = "large";
  }

  if (profiles.has("c")) {
    config.simplified = true;
    config.fontSize = config.fontSize === "large" ? "large" : "medium";
    config.tts = false;
  }

  if (profiles.has("a")) {
    config.captions = true;
  }

  if (profiles.has("m")) {
    config.largeButtons = true;
    config.singleSwitch = true;
    config.tts = false;
  }

  return config;
}

function applyConfig(config) {
  const root = document.documentElement;

  if (config.contrast) {
    root.style.setProperty("--bg", "#000000");
    root.style.setProperty("--text", "#ffffff");
    root.style.setProperty("--surface", "#111111");
    document.body.classList.add("high-contrast");
  }

  if (config.fontSize === "large") {
    document.body.classList.add("large-text");
    root.style.setProperty("--font-size-action", "26px");
  } else if (config.fontSize === "medium") {
    root.style.setProperty("--font-size-action", "20px");
  }

  if (config.simplified) {
    document.body.classList.add("simplified");
  }

  if (config.largeButtons) {
    document.body.classList.add("large-buttons");
  }
}
