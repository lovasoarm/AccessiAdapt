import tkinter as tk
from ui.theme import get_colors, PAD
from adapter import build_config
from modules.speech import speak
from modules.analytics import log_event

ACTIONS = ["Lire un message", "Écrire un message", "Paramètres", "Quitter"]


class ModeVisuel(tk.Frame):
    def __init__(self, master, profiles: set, on_back):
        config = build_config(profiles)
        self.c = get_colors(config["contrast"])
        super().__init__(master, bg=self.c["bg"])
        self.profiles    = profiles
        self.on_back     = on_back
        self.config_     = config
        self.fs          = config["font_size"]
        self.focus_index = 0
        self.items       = []
        self._build()
        self.after(100, lambda: self._set_focus(0))

    def _build(self):
        c, fs = self.c, self.fs

        tk.Label(self, text="MODE VISUEL", font=("Inter", 10),
                 bg=c["bg"], fg=c["sub"]).pack(anchor="w", padx=PAD, pady=(PAD, 4))

        tk.Label(self, text="Menu principal", font=("Inter", fs + 12, "bold"),
                 bg=c["bg"], fg=c["text"]).pack(anchor="w", padx=PAD, pady=(0, 6))

        tk.Label(self,
                 text="Navigue avec ↑ ↓ ou clique. Appuie sur Entrée pour valider.",
                 font=("Inter", fs), bg=c["surface"], fg=c["sub"],
                 padx=14, pady=12).pack(fill="x", padx=PAD, pady=(0, 16))

        self.tts_label = tk.Label(self, text='"Chargement..."',
                                  font=("Inter", fs - 2, "italic"),
                                  bg=c["surface"], fg=c["sub"], padx=14, pady=10)
        self.tts_label.pack(fill="x", padx=PAD, pady=(0, 10))

        self.focus_bar = tk.Label(self, text="Focus actuel : —",
                                  font=("Inter", 12), bg=c["surface"],
                                  fg=c["sub"], padx=14, pady=8)
        self.focus_bar.pack(fill="x", padx=PAD, pady=(0, 16))

        for i, label in enumerate(ACTIONS):
            self._make_item(i, label)

        self.feedback = tk.Label(self, text="", font=("Inter", fs),
                                 bg=c["surface"], fg=c["text"], padx=14, pady=12)

        sep = tk.Frame(self, height=1, bg=c["border"])
        sep.pack(fill="x", padx=PAD, pady=16)

        footer = tk.Frame(self, bg=c["bg"])
        footer.pack(fill="x", padx=PAD, pady=(0, PAD))

        tk.Label(footer, text="Mode contraste fort · Synthèse vocale active",
                 font=("Inter", 12), bg=c["bg"], fg=c["sub"]).pack(side="left")

        tk.Button(footer, text="Changer de profil", font=("Inter", 13),
                  bg=c["bg"], fg=c["text"], relief="solid",
                  bd=1, padx=16, pady=8, cursor="hand2",
                  command=self.on_back).pack(side="right")

        self.bind_all("<Up>",    lambda e: self._move(-1))
        self.bind_all("<Down>",  lambda e: self._move(1))
        self.bind_all("<Return>",lambda e: self._select(self.focus_index))

    def _make_item(self, i, label):
        c, fs = self.c, self.fs
        frame = tk.Frame(self, bg=c["surface"], cursor="hand2",
                         highlightbackground=c["border"], highlightthickness=1)
        frame.pack(fill="x", padx=PAD, pady=4)

        tk.Label(frame, text=label, font=("Inter", fs, "bold"),
                 bg=c["surface"], fg=c["text"],
                 padx=20, pady=18).pack(side="left", fill="x", expand=True)

        frame.bind("<Button-1>", lambda e, idx=i: self._select(idx))
        for child in frame.winfo_children():
            child.bind("<Button-1>", lambda e, idx=i: self._select(idx))

        self.items.append(frame)

    def _set_focus(self, i):
        self.focus_index = i
        c = self.c
        for idx, item in enumerate(self.items):
            on = idx == i
            border = c["text"] if on else c["border"]
            item.configure(highlightbackground=border,
                           highlightthickness=2 if on else 1)
        self.focus_bar.configure(text=f"Focus actuel : {ACTIONS[i]}")
        self.tts_label.configure(text=f'"{ACTIONS[i]}"')
        speak(ACTIONS[i])

    def _move(self, direction):
        nxt = (self.focus_index + direction) % len(ACTIONS)
        self._set_focus(nxt)

    def _select(self, i):
        log_event(self.profiles, ACTIONS[i])
        speak(ACTIONS[i] + " — ouvert")
        self.feedback.configure(text=ACTIONS[i] + " : ouvert")
        self.feedback.pack(fill="x", padx=PAD, pady=(0, 12))
        self.after(2500, lambda: self.feedback.pack_forget())