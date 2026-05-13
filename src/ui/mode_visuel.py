import tkinter as tk
from adapter import build_config, apply_config
from modules.speech import speak

class ModeVisuel(tk.Frame):
    def __init__(self, parent, app, profiles_str):
        super().__init__(parent, bg="#0e0e0c")
        self.app = app
        profiles = set(profiles_str.split(",")) if profiles_str else set()
        self.config = build_config(profiles)
        apply_config(self, self.config)

        container = tk.Frame(self, bg=self["bg"])
        container.pack(expand=True, padx=40, pady=40)

        title = tk.Label(container, text="Mode Visuel", font=("Inter", 12), fg="#8a8880", bg=self["bg"])
        title.pack(anchor="w")
        heading = tk.Label(container, text="Menu principal", font=("Inter", 28, "bold"), fg=self["fg"], bg=self["bg"])
        heading.pack(anchor="w", pady=(10,5))
        instr = tk.Label(container, text="Navigue avec les flèches ↑ ↓. Appuie sur Entrée pour valider.", font=("Inter", 14), fg="#8a8880", bg=self["bg"])
        instr.pack(anchor="w", pady=(0,20))

        self.tts_bar = tk.Frame(container, bg="#1a1a17", highlightbackground="#2c2c28", highlightthickness=1)
        self.tts_bar.pack(fill=tk.X, pady=10)
        dot = tk.Label(self.tts_bar, text="●", fg="#f0eee6", bg="#1a1a17", font=("Inter", 10))
        dot.pack(side=tk.LEFT, padx=12)
        self.tts_text = tk.Label(self.tts_bar, text='"Chargement..."', font=("Inter", 12, "italic"), fg="#8a8880", bg="#1a1a17")
        self.tts_text.pack(side=tk.LEFT)

        self.focus_bar = tk.Label(container, text="Focus actuel : —", font=("Inter", 12), fg="#8a8880", bg="#1a1a17", anchor="w", padx=10, pady=8)
        self.focus_bar.pack(fill=tk.X, pady=10)

        self.actions = ["Lire un message", "Écrire un message", "Paramètres", "Quitter"]
        self.action_frame = tk.Frame(container, bg=self["bg"])
        self.action_frame.pack(fill=tk.BOTH, expand=True)
        self.buttons = []
        self.current_focus = 0
        for i, action in enumerate(self.actions):
            btn = tk.Button(self.action_frame, text=action, font=("Inter", 16), bg="#1a1a17", fg=self["fg"],
                            relief=tk.FLAT, anchor="w", padx=20, pady=15,
                            command=lambda a=action, idx=i: self.select_action(idx))
            btn.pack(fill=tk.X, pady=5)
            self.buttons.append(btn)
        self.update_focus()

        self.feedback = tk.Label(container, text="", font=("Inter", 14), bg=self["bg"], fg="#f0eee6")
        self.feedback.pack(fill=tk.X, pady=10)

        footer = tk.Frame(container, bg=self["bg"])
        footer.pack(fill=tk.X, pady=20)
        hint = tk.Label(footer, text="Mode contraste fort · Synthèse vocale active", font=("Inter", 12), fg="#8a8880", bg=self["bg"])
        hint.pack(side=tk.LEFT)
        back_btn = tk.Button(footer, text="Changer de profil", command=self.go_back, bg="#1a1a17", fg=self["fg"], font=("Inter", 12))
        back_btn.pack(side=tk.RIGHT)

        self.bind_all("<Up>", lambda e: self.move_focus(-1))
        self.bind_all("<Down>", lambda e: self.move_focus(1))
        self.bind_all("<Return>", lambda e: self.select_action(self.current_focus))
        self.focus_set()

    def update_focus(self):
        for i, btn in enumerate(self.buttons):
            if i == self.current_focus:
                btn.config(highlightbackground="#f0eee6", highlightthickness=2)
            else:
                btn.config(highlightbackground="#2c2c28", highlightthickness=1)
        self.focus_bar.config(text=f"Focus actuel : {self.actions[self.current_focus]}")
        self.speak_text(self.actions[self.current_focus])

    def move_focus(self, delta):
        self.current_focus = (self.current_focus + delta) % len(self.actions)
        self.update_focus()
        self.buttons[self.current_focus].focus_set()

    def select_action(self, idx):
        action = self.actions[idx]
        if action == "Quitter":
            self.go_back()
            return
        self.speak_text(f"{action} — ouvert")
        self.feedback.config(text=f"{action} : ouvert")
        self.after(2500, lambda: self.feedback.config(text=""))

    def speak_text(self, text):
        self.tts_text.config(text=f'"{text}"')
        speak(text)

    def go_back(self):
        from ui.screen_select import ScreenSelect
        self.unbind_all("<Up>")
        self.unbind_all("<Down>")
        self.unbind_all("<Return>")
        self.app.current_frame.destroy()
        self.app.current_frame = ScreenSelect(self.app.root, self.app)
        self.app.current_frame.pack(fill=tk.BOTH, expand=True)