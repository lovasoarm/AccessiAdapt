def build_config(profiles_set):
    config = {
        "font_size": "normal",
        "contrast": False,
        "tts": False,
        "captions": False,
        "large_buttons": False,
        "single_switch": False,
        "simplified": False,
    }
    if "v" in profiles_set:
        config["contrast"] = True
        config["tts"] = True
        config["font_size"] = "large"
    if "c" in profiles_set:
        config["simplified"] = True
        if config["font_size"] != "large":
            config["font_size"] = "medium"
        config["tts"] = False
    if "a" in profiles_set:
        config["captions"] = True
    if "m" in profiles_set:
        config["large_buttons"] = True
        config["single_switch"] = True
        config["tts"] = False
    return config

def apply_config(widget, config):
    """
    Applique les configurations d'accessibilité à un widget Tkinter.
    Ignore les erreurs si le widget ne supporte pas une option.
    """
    if config.get("contrast", False):
        bg = "#000000"
        fg = "#ffffff"
    else:
        bg = "#0e0e0c"
        fg = "#f0eee6"

    # Appliquer bg (fond)
    try:
        widget.configure(bg=bg)
    except:
        pass

    # Appliquer fg (couleur du texte) si le widget le supporte
    try:
        widget.configure(fg=fg)
    except:
        pass

    # Gestion de la taille de police
    if config.get("font_size") == "large":
        font = ("Inter", 16)
    elif config.get("font_size") == "medium":
        font = ("Inter", 14)
    else:
        font = ("Inter", 12)

    try:
        widget.configure(font=font)
    except:
        pass

    # Pour les boutons, élargir si demandé
    if config.get("large_buttons", False):
        try:
            widget.configure(padx=30, pady=20)
        except:
            pass