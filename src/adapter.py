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
    if config["contrast"]:
        widget.configure(bg="#000000", fg="#ffffff")
    else:
        widget.configure(bg="#0e0e0c", fg="#f0eee6")
    if config["font_size"] == "large":
        widget.option_add("*Font", "Helvetica 14")