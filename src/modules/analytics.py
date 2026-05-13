import json
import os
from datetime import datetime

LOG_FILE = "usage_log.json"

def log_event(event_type, details=None):
    if details is None:
        details = {}
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "details": details
    }
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    logs.append(log_entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)