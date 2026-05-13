import tkinter as tk
from ui.theme import get_colors, PAD
from adapter import build_config
from modules.analytics import log_event

ACTIONS = ["Lire un message", "Écrire un message", "Paramètres", "Quitter"]


class ModeStandard(tk.Frame):
    def __init__(self, master, profiles: set, on_back):
        config = build_config(profiles)
        self.c = get_colors(config["contrast"])
        super().__init__(master, bg=self.c["bg"])
        self.profiles  = profiles
        self.on_back   = on_back
        self.config_   = config
        self.fs        = config["font_size"]
        self._build()

    def _build(self):
        c, fs = self.c, self.fs

        tk.Label(self, text="ACCESSIADAPT", font=("Inter", 10),
                 bg=c["bg"], fg=c["sub"]).pack(anchor="w", padx=PAD, pady=(PAD, 4))

        tk.Label(self, text="Menu principal", font=("Inter", fs + 14, "bold"),
                 bg=c["bg"], fg=c["text"]).pack(anchor="w", padx=PAD, pady=(0, 6))

        tk.Label(self, text="Choisis une action pour commencer.",
                 font=("Inter", fs), bg=c["surface"], fg=c["sub"],
                 padx=14, pady=12).pack(fill="x", padx=PAD, pady=(0, 20))

        for label in ACTIONS:
            self._make_item(label)

        self.feedback = tk.Label(self, text="", font=("Inter", fs),
                                 bg=c["surface"], fg=c["text"],
                                 padx=14, pady=12)

        sep = tk.Frame(self, height=1, bg=c["border"])
        sep.pack(fill="x", padx=PAD, pady=16)

        footer = tk.Frame(self, bg=c["bg"])
        footer.pack(fill="x", padx=PAD, pady=(0, PAD))

        tk.Label(footer, text="Mode standard", font=("Inter", 12),
                 bg=c["bg"], fg=c["sub"]).pack(side="left")

        tk.Button(footer, text="Changer de profil", font=("Inter", 13),
                  bg=c["bg"], fg=c["text"], relief="solid",
                  bd=1, padx=16, pady=8, cursor="hand2",
                  command=self.on_back).pack(side="right")

    def _make_item(self, label):
        c, fs = self.c, self.fs
        frame = tk.Frame(self, bg=c["surface"], cursor="hand2",
                         highlightbackground=c["border"], highlightthickness=1)
        frame.pack(fill="x", padx=PAD, pady=4)

        tk.Label(frame, text=label, font=("Inter", fs, "bold"),
                 bg=c["surface"], fg=c["text"],
                 padx=20, pady=16).pack(side="left")

        frame.bind("<Button-1>", lambda e, l=label: self._select(l))
        for child in frame.winfo_children():
            child.bind("<Button-1>", lambda e, l=label: self._select(l))

    def _select(self, label):
        log_event(self.profiles, label)
        if label == "Quitter":
            self.on_back()
            return
        self.feedback.configure(text=label + " : ouvert")
        self.feedback.pack(fill="x", padx=PAD, pady=(0, 12))
        self.after(2000, lambda: self.feedback.pack_forget())