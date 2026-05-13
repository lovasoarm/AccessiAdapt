PROFILES = {
    "v": {"name": "Visuel", "adapt": "Police 22px · Contraste noir/blanc · Synthèse vocale"},
    "m": {"name": "Moteur", "adapt": "Boutons larges · Balayage auto · Mono-bouton"},
    "a": {"name": "Auditif", "adapt": "Sous-titres · Alertes visuelles · Zéro dépendance audio"},
    "c": {"name": "Cognitif", "adapt": "Interface simple · 1 tâche par écran · Pictogrammes"},
}

def resolve_destination(selected_set):
    profiles = ",".join(selected_set)
    if "s" in selected_set or len(selected_set) >= 2:
        return "mode_standard", profiles
    if "m" in selected_set:
        return "mode_moteur", profiles
    if "v" in selected_set:
        return "mode_visuel", profiles
    if "c" in selected_set:
        return "mode_cognitif", profiles
    if "a" in selected_set:
        return "mode_auditif", profiles
    return "mode_standard", profiles