import json
import os
import time

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "usage.json")

def _ensure_log():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([], f)

def log_event(profiles: set, action: str, extra: dict = None):
    _ensure_log()
    with open(LOG_PATH, "r") as f:
        data = json.load(f)
    entry = {
        "timestamp": time.time(),
        "profiles":  list(profiles),
        "action":    action,
    }
    if extra:
        entry.update(extra)
    data.append(entry)
    with open(LOG_PATH, "w") as f:
        json.dump(data, f, indent=2)

def load_logs() -> list:
    _ensure_log()
    with open(LOG_PATH, "r") as f:
        return json.load(f)