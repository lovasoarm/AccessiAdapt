import tkinter as tk
from adapter import build_config

class ModeAuditif(tk.Frame):
    def __init__(self, parent, app, profiles_str):
        super().__init__(parent, bg="#0e0e0c")
        self.app = app
        profiles = set(profiles_str.split(",")) if profiles_str else set()
        self.config = build_config(profiles)
        if self.config.get("contrast"):
            self.bg_color = "#000000"
            self.fg_color = "#ffffff"
            self.surface_color = "#111111"
        else:
            self.bg_color = "#0e0e0c"
            self.fg_color = "#f0eee6"
            self.surface_color = "#1a1a17"
        self.configure(bg=self.bg_color)

        container = tk.Frame(self, bg=self.bg_color)
        container.pack(expand=True, padx=40, pady=40)

        title = tk.Label(container, text="Mode Auditif", font=("Inter", 12), fg="#8a8880", bg=self.bg_color)
        title.pack(anchor="w")
        heading = tk.Label(container, text="Menu principal", font=("Inter", 28, "bold"), fg=self.fg_color, bg=self.bg_color)
        heading.pack(anchor="w", pady=(10,5))
        instr = tk.Label(container, text="Toutes les informations sont affichées à l'écran. Aucune alerte sonore.", font=("Inter", 14), fg="#8a8880", bg=self.bg_color)
        instr.pack(anchor="w", pady=(0,20))

        status = tk.Frame(container, bg=self.surface_color, highlightbackground="#2c2c28", highlightthickness=1)
        status.pack(fill=tk.X, pady=10)
        dot = tk.Label(status, text="●", fg="#8a8880", bg=self.surface_color)
        dot.pack(side=tk.LEFT, padx=10)
        status_label = tk.Label(status, text="Son désactivé : toutes les alertes sont visuelles", font=("Inter", 12), fg="#8a8880", bg=self.surface_color)
        status_label.pack(side=tk.LEFT)

        self.actions = [
            {"label": "Lire un message", "subtitle": "Ouvre la liste de tes messages reçus."},
            {"label": "Écrire un message", "subtitle": "Compose et envoie un nouveau message."},
            {"label": "Paramètres", "subtitle": "Modifie ton profil et tes préférences."},
            {"label": "Quitter", "subtitle": "Ferme l'application AccessiAdapt."}
        ]
        self.action_frame = tk.Frame(container, bg=self.bg_color)
        self.action_frame.pack(fill=tk.BOTH, expand=True)
        self.buttons = []
        for i, action in enumerate(self.actions):
            btn = tk.Button(self.action_frame, text=action["label"], font=("Inter", 16), bg=self.surface_color, fg=self.fg_color,
                            relief=tk.FLAT, anchor="w", padx=20, pady=15,
                            command=lambda idx=i: self.select_action(idx))
            btn.pack(fill=tk.X, pady=5)
            btn.bind("<Enter>", lambda e, idx=i: self.show_subtitle(idx))
            self.buttons.append(btn)

        self.notif_frame = tk.Frame(container, bg=self.surface_color, highlightbackground="#2c2c28", highlightthickness=1)
        self.notif_frame.pack(fill=tk.X, pady=10)
        self.notif_label = tk.Label(self.notif_frame, text="", font=("Inter", 14), fg=self.fg_color, bg=self.surface_color)
        self.notif_label.pack(padx=10, pady=10)
        self.notif_frame.pack_forget()

        self.subtitle_frame = tk.Frame(container, bg=self.surface_color, highlightbackground="#2c2c28", highlightthickness=1)
        self.subtitle_frame.pack(fill=tk.X, pady=10)
        sub_label = tk.Label(self.subtitle_frame, text="Description", font=("Inter", 10, "bold"), fg="#8a8880", bg=self.surface_color)
        sub_label.pack(anchor="w", padx=10, pady=(10,0))
        self.subtitle_text = tk.Label(self.subtitle_frame, text="Survole ou clique sur une action pour voir sa description.", font=("Inter", 12), fg=self.fg_color, bg=self.surface_color, wraplength=500, justify=tk.LEFT)
        self.subtitle_text.pack(anchor="w", padx=10, pady=(0,10))

        footer = tk.Frame(container, bg=self.bg_color)
        footer.pack(fill=tk.X, pady=20)
        hint = tk.Label(footer, text="Mode visuel uniquement · Zéro dépendance audio", font=("Inter", 12), fg="#8a8880", bg=self.bg_color)
        hint.pack(side=tk.LEFT)
        back_btn = tk.Button(footer, text="Changer de profil", command=self.go_back, bg=self.surface_color, fg=self.fg_color, font=("Inter", 12))
        back_btn.pack(side=tk.RIGHT)

    def show_subtitle(self, idx):
        self.subtitle_text.config(text=self.actions[idx]["subtitle"])

    def select_action(self, idx):
        action = self.actions[idx]
        if action["label"] == "Quitter":
            self.go_back()
            return
        self.show_notif(f"{action['label']} : ouvert")
        self.show_subtitle(idx)

    def show_notif(self, text):
        self.notif_label.config(text=text)
        self.notif_frame.pack(fill=tk.X, pady=10, before=self.subtitle_frame)
        self.after(3000, lambda: self.notif_frame.pack_forget())

    def go_back(self):
        from ui.screen_select import ScreenSelect
        self.app.current_frame.destroy()
        self.app.current_frame = ScreenSelect(self.app.root, self.app)
        self.app.current_frame.pack(fill=tk.BOTH, expand=True)