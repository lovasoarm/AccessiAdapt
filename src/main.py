import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from ui.screen_select import ScreenSelect

class AccessiAdaptApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AccessiAdapt")
        self.root.geometry("800x600")
        self.root.configure(bg="#0e0e0c")
        self.current_frame = None
        self.show_screen_select()

    def show_screen_select(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ScreenSelect(self.root, self)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AccessiAdaptApp()
    app.run()