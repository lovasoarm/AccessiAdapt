PROFILES = {
    "v": {"name": "Visuel",   "desc": "Je vois mal ou pas bien les couleurs."},
    "m": {"name": "Moteur",   "desc": "J'ai du mal à cliquer ou à bouger la souris."},
    "a": {"name": "Auditif",  "desc": "Je n'entends pas bien ou pas du tout."},
    "c": {"name": "Cognitif", "desc": "Je me perds vite si c'est trop chargé."},
    "s": {"name": "Standard", "desc": "Plusieurs besoins, ou je configure moi-même."},
}

PRIORITY = ["m", "v", "c", "a"]

def resolve_destination(selected: set) -> str:
    if "s" in selected or len(selected) >= 2:
        return "standard"
    for key in PRIORITY:
        if key in selected:
            return key
    return "standard"