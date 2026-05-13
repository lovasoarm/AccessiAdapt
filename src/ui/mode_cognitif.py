import tkinter as tk
from adapter import build_config, apply_config

class ModeCognitif(tk.Frame):
    def __init__(self, parent, app, profiles_str):
        super().__init__(parent, bg="#0e0e0c")
        self.app = app
        profiles = set(profiles_str.split(",")) if profiles_str else set()
        self.config = build_config(profiles)
        apply_config(self, self.config)

        container = tk.Frame(self, bg=self["bg"])
        container.pack(expand=True, padx=40, pady=40)

        title = tk.Label(container, text="Mode Cognitif", font=("Inter", 12), fg="#8a8880", bg=self["bg"])
        title.pack(anchor="w")
        heading = tk.Label(container, text="Que veux-tu faire ?", font=("Inter", 28, "bold"), fg=self["fg"], bg=self["bg"])
        heading.pack(anchor="w", pady=(10,5))
        instr = tk.Label(container, text="Choisis une seule action. Je t'aide ensuite étape par étape.", font=("Inter", 14), fg="#8a8880", bg=self["bg"])
        instr.pack(anchor="w", pady=(0,20))

        step_frame = tk.Frame(container, bg=self["bg"])
        step_frame.pack(fill=tk.X, pady=10)
        self.step_label = tk.Label(step_frame, text="Choix de l'action", font=("Inter", 12), fg="#8a8880", bg=self["bg"])
        self.step_label.pack(side=tk.LEFT)
        self.step_dots_frame = tk.Frame(step_frame, bg=self["bg"])
        self.step_dots_frame.pack(side=tk.RIGHT)

        self.guide_box = tk.Label(container, text="", font=("Inter", 14), bg="#1a1a17", fg="#8a8880", wraplength=500, justify=tk.LEFT, anchor="w", padx=15, pady=15)
        self.guide_box.pack(fill=tk.X, pady=10)

        self.actions = [
            {"label": "Lire", "guide": "Tu vas voir tes messages reçus. Une liste simple, un message à la fois.", "icon": "📖"},
            {"label": "Écrire", "guide": "Tu vas écrire un message. On t'aide étape par étape.", "icon": "✏️"},
            {"label": "Paramètres", "guide": "Tu peux changer ton profil ou la vitesse de l'interface.", "icon": "⚙️"},
            {"label": "Quitter", "guide": "L'application va se fermer. Tes données sont sauvegardées.", "icon": "🚪"}
        ]
        self.action_frame = tk.Frame(container, bg=self["bg"])
        self.action_frame.pack(fill=tk.BOTH, expand=True)
        self.buttons = []
        for i, action in enumerate(self.actions):
            btn_frame = tk.Frame(self.action_frame, bg="#1a1a17", highlightbackground="#2c2c28", highlightthickness=1)
            btn_frame.pack(fill=tk.X, pady=5)
            icon_lbl = tk.Label(btn_frame, text=action["icon"], font=("Inter", 20), bg="#1a1a17", fg=self["fg"])
            icon_lbl.pack(side=tk.LEFT, padx=15)
            text_lbl = tk.Label(btn_frame, text=action["label"], font=("Inter", 16), bg="#1a1a17", fg=self["fg"])
            text_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)
            arrow = tk.Label(btn_frame, text="→", font=("Inter", 16), bg="#1a1a17", fg="#8a8880")
            arrow.pack(side=tk.RIGHT, padx=15)
            btn_frame.bind("<Button-1>", lambda e, idx=i: self.select_action(idx))
            icon_lbl.bind("<Button-1>", lambda e, idx=i: self.select_action(idx))
            text_lbl.bind("<Button-1>", lambda e, idx=i: self.select_action(idx))
            arrow.bind("<Button-1>", lambda e, idx=i: self.select_action(idx))
            btn_frame.bind("<Enter>", lambda e, idx=i: self.update_guide(idx))
            self.buttons.append(btn_frame)

        self.feedback = tk.Label(container, text="", font=("Inter", 14), bg=self["bg"], fg="#f0eee6")
        self.feedback.pack(fill=tk.X, pady=10)

        footer = tk.Frame(container, bg=self["bg"])
        footer.pack(fill=tk.X, pady=20)
        hint = tk.Label(footer, text="Interface simplifiée · Guidage pas à pas", font=("Inter", 12), fg="#8a8880", bg=self["bg"])
        hint.pack(side=tk.LEFT)
        back_btn = tk.Button(footer, text="Changer de profil", command=self.go_back, bg="#1a1a17", fg=self["fg"], font=("Inter", 12))
        back_btn.pack(side=tk.RIGHT)

        self.update_guide(-1)
        self.update_step_dots(0)

    def update_guide(self, idx):
        if idx == -1:
            self.guide_box.config(text="Choisis une action. Prends ton temps, il n'y a pas d'urgence.")
        else:
            self.guide_box.config(text=self.actions[idx]["guide"])
            self.update_step_dots(idx)

    def update_step_dots(self, idx):
        for widget in self.step_dots_frame.winfo_children():
            widget.destroy()
        for i in range(len(self.actions)):
            dot = tk.Label(self.step_dots_frame, text="●", font=("Inter", 10), fg=self["fg"] if i == idx else "#2c2c28", bg=self["bg"])
            dot.pack(side=tk.LEFT, padx=2)
        self.step_label.config(text=f"Étape {idx+1} sur {len(self.actions)}" if idx >= 0 else "Choix de l'action")

    def select_action(self, idx):
        action = self.actions[idx]
        if action["label"] == "Quitter":
            self.go_back()
            return
        self.feedback.config(text=f"{action['label']} : c'est parti.")
        self.after(2500, lambda: self.feedback.config(text=""))

    def go_back(self):
        from ui.screen_select import ScreenSelect
        self.app.current_frame.destroy()
        self.app.current_frame = ScreenSelect(self.app.root, self.app)
        self.app.current_frame.pack(fill=tk.BOTH, expand=True)