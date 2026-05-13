import tkinter as tk
from adapter import build_config
from modules.scanner import Scanner

class ModeMoteur(tk.Frame):
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

        title = tk.Label(container, text="Mode Moteur", font=("Inter", 12), fg="#8a8880", bg=self.bg_color)
        title.pack(anchor="w")
        heading = tk.Label(container, text="Menu principal", font=("Inter", 28, "bold"), fg=self.fg_color, bg=self.bg_color)
        heading.pack(anchor="w", pady=(10,5))
        instr = tk.Label(container, text="Le curseur défile automatiquement. Appuie sur Valider ou sur Espace.", font=("Inter", 14), fg="#8a8880", bg=self.bg_color)
        instr.pack(anchor="w", pady=(0,20))

        speed_frame = tk.Frame(container, bg=self.surface_color, highlightbackground="#2c2c28", highlightthickness=1)
        speed_frame.pack(fill=tk.X, pady=10)
        speed_label = tk.Label(speed_frame, text="Vitesse : ", font=("Inter", 12), fg="#8a8880", bg=self.surface_color)
        speed_label.pack(side=tk.LEFT, padx=10)
        self.speed_var = tk.IntVar(value=3)
        self.speed_scale = tk.Scale(speed_frame, from_=1, to=5, orient=tk.HORIZONTAL, variable=self.speed_var,
                                    bg=self.surface_color, fg=self.fg_color, highlightthickness=0, command=self.change_speed)
        self.speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.speed_label_val = tk.Label(speed_frame, text="Normale", font=("Inter", 12), fg=self.fg_color, bg=self.surface_color)
        self.speed_label_val.pack(side=tk.RIGHT, padx=10)

        self.actions = ["Lire un message", "Écrire un message", "Paramètres", "Quitter"]
        self.action_frame = tk.Frame(container, bg=self.bg_color)
        self.action_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.buttons = []
        for action in self.actions:
            btn = tk.Button(self.action_frame, text=action, font=("Inter", 16), bg=self.surface_color, fg=self.fg_color,
                            relief=tk.FLAT, anchor="w", padx=20, pady=15, state=tk.DISABLED)
            btn.pack(fill=tk.X, pady=5)
            self.buttons.append(btn)

        self.scan_label = tk.Label(container, text="En surbrillance : —", font=("Inter", 12), fg="#8a8880", bg=self.surface_color, anchor="w", padx=10, pady=8)
        self.scan_label.pack(fill=tk.X, pady=10)

        validate_btn = tk.Button(container, text="Valider", command=self.validate, bg=self.fg_color, fg=self.bg_color,
                                 font=("Inter", 16, "bold"), padx=30, pady=12)
        validate_btn.pack(pady=10)

        self.feedback = tk.Label(container, text="", font=("Inter", 14), bg=self.bg_color, fg=self.fg_color)
        self.feedback.pack(fill=tk.X, pady=10)

        footer = tk.Frame(container, bg=self.bg_color)
        footer.pack(fill=tk.X, pady=20)
        hint = tk.Label(footer, text="Mode mono-bouton · Balayage automatique", font=("Inter", 12), fg="#8a8880", bg=self.bg_color)
        hint.pack(side=tk.LEFT)
        back_btn = tk.Button(footer, text="Changer de profil", command=self.go_back, bg=self.surface_color, fg=self.fg_color, font=("Inter", 12))
        back_btn.pack(side=tk.RIGHT)

        self.scanner = Scanner(self.buttons, self.scan_label, self.actions)
        self.scanner.start(self.get_speed_ms())

        self.bind_all("<space>", lambda e: self.validate())
        self.bind_all("<Return>", lambda e: self.validate())
        self.focus_set()

    def get_speed_ms(self):
        val = self.speed_var.get()
        return 2600 - val * 400

    def change_speed(self, _):
        speeds = ["Très lente", "Lente", "Normale", "Rapide", "Très rapide"]
        self.speed_label_val.config(text=speeds[self.speed_var.get()-1])
        self.scanner.set_interval(self.get_speed_ms())

    def validate(self):
        selected = self.scanner.get_current()
        if not selected:
            return
        if selected == "Quitter":
            self.go_back()
            return
        self.feedback.config(text=f"{selected} : sélectionné")
        self.after(2000, lambda: self.feedback.config(text=""))

    def go_back(self):
        self.scanner.stop()
        self.unbind_all("<space>")
        self.unbind_all("<Return>")
        from ui.screen_select import ScreenSelect
        self.app.current_frame.destroy()
        self.app.current_frame = ScreenSelect(self.app.root, self.app)
        self.app.current_frame.pack(fill=tk.BOTH, expand=True)