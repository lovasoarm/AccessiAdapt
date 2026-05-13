import tkinter as tk

class Scanner:
    def __init__(self, buttons, label_widget, actions):
        self.buttons = buttons
        self.label_widget = label_widget
        self.actions = actions
        self.current_index = 0
        self.timer = None
        self.interval = 1500

    def start(self, interval_ms=None):
        if interval_ms:
            self.interval = interval_ms
        self.stop()
        self._schedule()

    def _schedule(self):
        self.timer = self.buttons[0].after(self.interval, self._advance)

    def _advance(self):
        self.current_index = (self.current_index + 1) % len(self.buttons)
        self._highlight_current()
        self.timer = self.buttons[0].after(self.interval, self._advance)

    def _highlight_current(self):
        for i, btn in enumerate(self.buttons):
            if i == self.current_index:
                btn.config(highlightbackground="#f0eee6", highlightthickness=2, state=tk.NORMAL)
            else:
                btn.config(highlightbackground="#2c2c28", highlightthickness=1, state=tk.DISABLED)
        self.label_widget.config(text=f"En surbrillance : {self.actions[self.current_index]}")

    def set_interval(self, new_interval):
        self.interval = new_interval
        self.restart()

    def restart(self):
        if self.timer:
            self.buttons[0].after_cancel(self.timer)
        self._highlight_current()
        self._schedule()

    def get_current(self):
        return self.actions[self.current_index]

    def stop(self):
        if self.timer:
            self.buttons[0].after_cancel(self.timer)
            self.timer = None