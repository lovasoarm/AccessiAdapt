import tkinter as tk
from adapter import build_config

class ModeStandard(tk.Frame):
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

        title = tk.Label(container, text="AccessiAdapt", font=("Inter", 12), fg="#8a8880", bg=self.bg_color)
        title.pack(anchor="w")
        heading = tk.Label(container, text="Menu principal", font=("Inter", 28, "bold"), fg=self.fg_color, bg=self.bg_color)
        heading.pack(anchor="w", pady=(10,5))
        instr = tk.Label(container, text="Choisis une action pour commencer.", font=("Inter", 14), fg="#8a8880", bg=self.bg_color)
        instr.pack(anchor="w", pady=(0,20))

        self.actions = ["Lire un message", "Écrire un message", "Paramètres", "Quitter"]
        self.action_frame = tk.Frame(container, bg=self.bg_color)
        self.action_frame.pack(fill=tk.BOTH, expand=True)
        self.widgets = []
        for action in self.actions:
            btn = tk.Button(self.action_frame, text=action, font=("Inter", 16), bg=self.surface_color, fg=self.fg_color,
                            relief=tk.FLAT, anchor="w", padx=20, pady=15, command=lambda a=action: self.select_action(a))
            btn.pack(fill=tk.X, pady=5)
            self.widgets.append(btn)

        self.feedback = tk.Label(container, text="", font=("Inter", 14), bg=self.bg_color, fg=self.fg_color)
        self.feedback.pack(fill=tk.X, pady=10)

        footer = tk.Frame(container, bg=self.bg_color)
        footer.pack(fill=tk.X, pady=20)
        hint = tk.Label(footer, text="Mode standard", font=("Inter", 12), fg="#8a8880", bg=self.bg_color)
        hint.pack(side=tk.LEFT)
        back_btn = tk.Button(footer, text="Changer de profil", command=self.go_back, bg=self.surface_color, fg=self.fg_color, font=("Inter", 12))
        back_btn.pack(side=tk.RIGHT)

    def select_action(self, action):
        if action == "Quitter":
            self.go_back()
            return
        self.feedback.config(text=f"{action} : ouvert")
        self.after(2000, lambda: self.feedback.config(text=""))

    def go_back(self):
        from ui.screen_select import ScreenSelect
        self.app.current_frame.destroy()
        self.app.current_frame = ScreenSelect(self.app.root, self.app)
        self.app.current_frame.pack(fill=tk.BOTH, expand=True)