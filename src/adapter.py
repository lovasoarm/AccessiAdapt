def build_config(profiles: set) -> dict:
    config = {
        "font_size":    14,
        "contrast":     False,
        "tts":          False,
        "captions":     False,
        "large_buttons":False,
        "single_switch":False,
        "simplified":   False,
        "scan_speed":   1500,
    }

    if "v" in profiles:
        config["contrast"]   = True
        config["tts"]        = True
        config["font_size"]  = 22

    if "c" in profiles:
        config["simplified"] = True
        config["font_size"]  = max(config["font_size"], 18)
        config["tts"]        = False

    if "a" in profiles:
        config["captions"]   = True

    if "m" in profiles:
        config["large_buttons"] = True
        config["single_switch"] = True
        config["font_size"]     = max(config["font_size"], 20)
        config["tts"]           = False

    return config


def apply_theme(root, config: dict):
    if config["contrast"]:
        root.configure(bg="#000000")
    else:
        root.configure(bg="#0e0e0c")