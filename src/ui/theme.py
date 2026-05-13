DARK = {
    "bg":       "#0e0e0c",
    "surface":  "#1a1a17",
    "border":   "#2c2c28",
    "text":     "#f0eee6",
    "sub":      "#8a8880",
    "muted":    "#555350",
    "on_bg":    "#242420",
}

CONTRAST = {
    "bg":       "#000000",
    "surface":  "#111111",
    "border":   "#444444",
    "text":     "#ffffff",
    "sub":      "#aaaaaa",
    "muted":    "#666666",
    "on_bg":    "#1a1a1a",
}

FONT_NORMAL = ("Inter", 14)
FONT_MEDIUM = ("Inter", 18)
FONT_LARGE  = ("Inter", 22)
FONT_TITLE  = ("Inter", 28, "bold")
FONT_APPNAME = ("Inter", 10)

RADIUS = 10
PAD    = 24


def get_colors(contrast: bool) -> dict:
    return CONTRAST if contrast else DARK