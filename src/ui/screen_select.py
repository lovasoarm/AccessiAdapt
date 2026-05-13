import tkinter as tk
from tkinter import font
from profile import PROFILES, resolve_destination
from adapter import build_config

class ScreenSelect(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#0e0e0c")
        self.app = app
        self.selected = set()

        container = tk.Frame(self, bg="#0e0e0c")
        container.pack(expand=True, padx=40, pady=40)

        title = tk.Label(container, text="AccessiAdapt", font=("Inter", 12), fg="#8a8880", bg="#0e0e0c")
        title.pack(anchor="w", pady=(0,16))

        heading = tk.Label(container, text="Quel est ton profil ?", font=("Inter", 28, "bold"), fg="#f0eee6", bg="#0e0e0c")
        heading.pack(anchor="w")

        instr_frame = tk.Frame(container, bg="#1a1a17", highlightbackground="#2c2c28", highlightthickness=1)
        instr_frame.pack(fill=tk.X, pady=20)
        instr = tk.Label(instr_frame, text="Clique sur le profil qui te correspond. Tu peux en choisir plusieurs.", font=("Inter", 14), fg="#8a8880", bg="#1a1a17")
        instr.pack(padx=18, pady=14, anchor="w")

        self.grid_frame = tk.Frame(container, bg="#0e0e0c")
        self.grid_frame.pack(fill=tk.BOTH, expand=True)

        self.cards = {}
        for key, data in PROFILES.items():
            card = self.make_card(key, data["name"], data["adapt"])
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.std_card = self.make_standard_card()
        self.std_card.pack(fill=tk.X, pady=20)

        self.footer = tk.Frame(container, bg="#0e0e0c")
        self.footer.pack(fill=tk.X, pady=20)
        self.hint_label = tk.Label(self.footer, text="Sélectionne au moins un profil pour continuer.", font=("Inter", 12), fg="#8a8880", bg="#0e0e0c")
        self.hint_label.pack(side=tk.LEFT)
        self.continue_btn = tk.Button(self.footer, text="Continuer", state=tk.DISABLED, command=self.launch_app, bg="#f0eee6", fg="#0e0e0c", font=("Inter", 12, "bold"), padx=20, pady=8)
        self.continue_btn.pack(side=tk.RIGHT)

    def make_card(self, key, name, desc):
        frame = tk.Frame(self.grid_frame, bg="#1a1a17", highlightbackground="#2c2c28", highlightthickness=1, relief=tk.FLAT)
        frame._chk = tk.Label(frame, text="✓", fg="#0e0e0c", bg="#1a1a17", font=("Inter", 12))
        frame._chk.pack(side=tk.RIGHT, padx=10, pady=10)
        frame._chk.place_forget()

        name_lbl = tk.Label(frame, text=name, font=("Inter", 18, "bold"), fg="#f0eee6", bg="#1a1a17")
        name_lbl.pack(anchor="w", padx=20, pady=(20,5))
        desc_lbl = tk.Label(frame, text=desc, font=("Inter", 12), fg="#8a8880", bg="#1a1a17", wraplength=150)
        desc_lbl.pack(anchor="w", padx=20, pady=(0,20))

        frame.bind("<Button-1>", lambda e, k=key: self.toggle_profile(k))
        name_lbl.bind("<Button-1>", lambda e, k=key: self.toggle_profile(k))
        desc_lbl.bind("<Button-1>", lambda e, k=key: self.toggle_profile(k))
        return frame

    def make_standard_card(self):
        frame = tk.Frame(self.grid_frame, bg="#1a1a17", highlightbackground="#2c2c28", highlightthickness=1)
        chk = tk.Label(frame, text="✓", fg="#0e0e0c", bg="#1a1a17")
        chk.pack(side=tk.RIGHT, padx=10, pady=10)
        chk.place_forget()

        icon = tk.Label(frame, text="⚙️", font=("Inter", 20), bg="#1a1a17", fg="#8a8880")
        icon.pack(side=tk.LEFT, padx=16)
        text_frame = tk.Frame(frame, bg="#1a1a17")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        name_lbl = tk.Label(text_frame, text="Standard ou combiné", font=("Inter", 14, "bold"), fg="#f0eee6", bg="#1a1a17")
        name_lbl.pack(anchor="w")
        sub_lbl = tk.Label(text_frame, text="Plusieurs besoins, ou je configure moi-même.", font=("Inter", 11), fg="#8a8880", bg="#1a1a17")
        sub_lbl.pack(anchor="w")

        frame.bind("<Button-1>", lambda e: self.toggle_standard())
        name_lbl.bind("<Button-1>", lambda e: self.toggle_standard())
        sub_lbl.bind("<Button-1>", lambda e: self.toggle_standard())
        icon.bind("<Button-1>", lambda e: self.toggle_standard())
        frame._chk = chk
        return frame

    def toggle_profile(self, key):
        if "s" in self.selected:
            self.selected.remove("s")
            self.set_card_selected(self.std_card, False)
        if key in self.selected:
            self.selected.remove(key)
            self.set_card_selected(self.cards[key], False)
        else:
            self.selected.add(key)
            self.set_card_selected(self.cards[key], True)
        self.update_footer()

    def toggle_standard(self):
        for k in list(self.selected):
            if k != "s":
                self.selected.discard(k)
                self.set_card_selected(self.cards[k], False)
        if "s" in self.selected:
            self.selected.remove("s")
            self.set_card_selected(self.std_card, False)
        else:
            self.selected.add("s")
            self.set_card_selected(self.std_card, True)
        self.update_footer()

    def set_card_selected(self, card, selected):
        if selected:
            card.configure(highlightbackground="#f0eee6", highlightthickness=2)
            card._chk.place(relx=1, x=-10, y=10, anchor="ne")
        else:
            card.configure(highlightbackground="#2c2c28", highlightthickness=1)
            card._chk.place_forget()

    def update_footer(self):
        if len(self.selected) == 0:
            self.continue_btn.config(state=tk.DISABLED)
            self.hint_label.config(text="Sélectionne au moins un profil pour continuer.")
        else:
            self.continue_btn.config(state=tk.NORMAL)
            if "s" in self.selected:
                self.hint_label.config(text="Mode standard sélectionné.")
            else:
                names = [PROFILES[k]["name"] for k in self.selected]
                if len(names) == 1:
                    self.hint_label.config(text=f"Profil {names[0]} sélectionné.")
                else:
                    self.hint_label.config(text=f"Profil combiné : {' + '.join(names)}.")

    def launch_app(self):
        mode, profiles_str = resolve_destination(self.selected)
        if mode == "mode_standard":
            from ui.mode_standard import ModeStandard
            self.app.current_frame.destroy()
            self.app.current_frame = ModeStandard(self.app.root, self.app, profiles_str)
            self.app.current_frame.pack(fill=tk.BOTH, expand=True)
        elif mode == "mode_visuel":
            from ui.mode_visuel import ModeVisuel
            self.app.current_frame.destroy()
            self.app.current_frame = ModeVisuel(self.app.root, self.app, profiles_str)
            self.app.current_frame.pack(fill=tk.BOTH, expand=True)
        elif mode == "mode_moteur":
            from ui.mode_moteur import ModeMoteur
            self.app.current_frame.destroy()
            self.app.current_frame = ModeMoteur(self.app.root, self.app, profiles_str)
            self.app.current_frame.pack(fill=tk.BOTH, expand=True)
        elif mode == "mode_auditif":
            from ui.mode_auditif import ModeAuditif
            self.app.current_frame.destroy()
            self.app.current_frame = ModeAuditif(self.app.root, self.app, profiles_str)
            self.app.current_frame.pack(fill=tk.BOTH, expand=True)
        elif mode == "mode_cognitif":
            from ui.mode_cognitif import ModeCognitif
            self.app.current_frame.destroy()
            self.app.current_frame = ModeCognitif(self.app.root, self.app, profiles_str)
            self.app.current_frame.pack(fill=tk.BOTH, expand=True)