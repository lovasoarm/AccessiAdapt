import tkinter as tk
from ui.theme import get_colors, FONT_TITLE, FONT_NORMAL, FONT_APPNAME, PAD
from profile import PROFILES, resolve_destination


class ScreenSelect(tk.Frame):
    def __init__(self, master, on_launch):
        super().__init__(master, bg=get_colors(False)["bg"])
        self.master     = master
        self.on_launch  = on_launch
        self.selected   = set()
        self.c          = get_colors(False)
        self.card_widgets = {}
        self._build()

    def _build(self):
        self.configure(bg=self.c["bg"])

        tk.Label(self, text="ACCESSIADAPT", font=FONT_APPNAME,
                 bg=self.c["bg"], fg=self.c["sub"]).pack(anchor="w", padx=PAD, pady=(PAD, 4))

        tk.Label(self, text="Quel est ton profil ?", font=FONT_TITLE,
                 bg=self.c["bg"], fg=self.c["text"]).pack(anchor="w", padx=PAD, pady=(0, 6))

        tk.Label(self, text="Clique sur le profil qui te correspond. Tu peux en choisir plusieurs.",
                 font=FONT_NORMAL, bg=self.c["surface"], fg=self.c["sub"],
                 wraplength=580, justify="left", padx=14, pady=12).pack(
                     fill="x", padx=PAD, pady=(0, 20))

        grid_frame = tk.Frame(self, bg=self.c["bg"])
        grid_frame.pack(fill="x", padx=PAD)

        profile_keys = ["v", "m", "a", "c"]
        for idx, key in enumerate(profile_keys):
            row, col = divmod(idx, 2)
            card = self._make_card(grid_frame, key)
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.card_widgets[key] = card
            grid_frame.columnconfigure(col, weight=1)

        std_card = self._make_std_card()
        std_card.pack(fill="x", padx=PAD, pady=(10, 0))
        self.card_widgets["s"] = std_card

        sep = tk.Frame(self, height=1, bg=self.c["border"])
        sep.pack(fill="x", padx=PAD, pady=20)

        footer = tk.Frame(self, bg=self.c["bg"])
        footer.pack(fill="x", padx=PAD, pady=(0, PAD))

        self.hint_var = tk.StringVar(value="Sélectionne au moins un profil pour continuer.")
        self.hint_label = tk.Label(footer, textvariable=self.hint_var,
                                   font=("Inter", 13), bg=self.c["bg"],
                                   fg=self.c["sub"], wraplength=380, justify="left")
        self.hint_label.pack(side="left", fill="x", expand=True)

        self.btn_continue = tk.Button(footer, text="Continuer",
                                      font=("Inter", 14, "bold"),
                                      bg=self.c["text"], fg=self.c["bg"],
                                      relief="flat", padx=24, pady=10,
                                      cursor="hand2", state="disabled",
                                      command=self._launch)
        self.btn_continue.pack(side="right")

    def _make_card(self, parent, key):
        p = PROFILES[key]
        c = self.c
        frame = tk.Frame(parent, bg=c["surface"], cursor="hand2",
                         highlightbackground=c["border"], highlightthickness=1)

        top = tk.Frame(frame, bg=c["surface"])
        top.pack(fill="x", padx=16, pady=(16, 4))

        tk.Label(top, text=p["name"], font=("Inter", 20, "bold"),
                 bg=c["surface"], fg=c["text"]).pack(side="left")

        chk = tk.Label(top, text="✓", font=("Inter", 12, "bold"),
                       bg=c["surface"], fg=c["surface"],
                       width=2, relief="groove")
        chk.pack(side="right")
        frame._chk = chk

        tk.Label(frame, text=p["desc"], font=("Inter", 12),
                 bg=c["surface"], fg=c["sub"], wraplength=220,
                 justify="left").pack(anchor="w", padx=16, pady=(4, 16))

        frame.bind("<Button-1>", lambda e, k=key: self._toggle(k))
        for child in frame.winfo_children():
            child.bind("<Button-1>", lambda e, k=key: self._toggle(k))
            for gc in child.winfo_children():
                gc.bind("<Button-1>", lambda e, k=key: self._toggle(k))

        return frame

    def _make_std_card(self):
        c = self.c
        frame = tk.Frame(self, bg=c["surface"], cursor="hand2",
                         highlightbackground=c["border"], highlightthickness=1)

        inner = tk.Frame(frame, bg=c["surface"])
        inner.pack(fill="x", padx=16, pady=14)

        tk.Label(inner, text="Standard ou combiné", font=("Inter", 15, "bold"),
                 bg=c["surface"], fg=c["text"]).pack(side="left")

        chk = tk.Label(inner, text="✓", font=("Inter", 12, "bold"),
                       bg=c["surface"], fg=c["surface"], width=2, relief="groove")
        chk.pack(side="right")
        frame._chk = chk

        tk.Label(frame, text="Plusieurs besoins, ou je configure moi-même.",
                 font=("Inter", 12), bg=c["surface"], fg=c["sub"]).pack(
                     anchor="w", padx=16, pady=(0, 14))

        frame.bind("<Button-1>", lambda e: self._toggle_std())
        for child in frame.winfo_children():
            child.bind("<Button-1>", lambda e: self._toggle_std())
            for gc in child.winfo_children():
                gc.bind("<Button-1>", lambda e: self._toggle_std())

        return frame

    def _toggle(self, key):
        if "s" in self.selected:
            self._set_card("s", False)
            self.selected.discard("s")

        if key in self.selected:
            self.selected.discard(key)
            self._set_card(key, False)
        else:
            self.selected.add(key)
            self._set_card(key, True)

        self._update_footer()

    def _toggle_std(self):
        self.selected.clear()
        for k in ["v", "m", "a", "c"]:
            self._set_card(k, False)

        was_on = "s" in self.selected
        if not was_on:
            self.selected.add("s")
            self._set_card("s", True)
        else:
            self._set_card("s", False)

        self._update_footer()

    def _set_card(self, key, on: bool):
        card = self.card_widgets.get(key)
        if not card:
            return
        c = self.c
        bg = c["on_bg"] if on else c["surface"]
        border = c["text"] if on else c["border"]
        card.configure(bg=bg, highlightbackground=border,
                       highlightthickness=2 if on else 1)
        for child in card.winfo_children():
            child.configure(bg=bg)
            for gc in child.winfo_children():
                try:
                    gc.configure(bg=bg)
                except Exception:
                    pass
        card._chk.configure(fg=c["text"] if on else bg)

    def _update_footer(self):
        if not self.selected:
            self.btn_continue.configure(state="disabled")
            self.hint_var.set("Sélectionne au moins un profil pour continuer.")
            return

        self.btn_continue.configure(state="normal")

        if "s" in self.selected:
            self.hint_var.set("Mode standard sélectionné.")
            return

        names = [PROFILES[k]["name"] for k in self.selected]
        if len(names) == 1:
            self.hint_var.set(f"Profil {names[0]} sélectionné.")
        else:
            self.hint_var.set("Profil combiné : " + " + ".join(names) + ".")

    def _launch(self):
        self.on_launch(self.selected.copy())