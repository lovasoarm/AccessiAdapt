class Scanner:
    def __init__(self, items: list, on_highlight, speed_ms: int = 1500):
        self.items      = items
        self.on_highlight = on_highlight
        self.speed_ms   = speed_ms
        self.index      = 0
        self._job       = None
        self._root      = None

    def start(self, root):
        self._root = root
        self._tick()

    def stop(self):
        if self._job and self._root:
            self._root.after_cancel(self._job)
            self._job = None

    def set_speed(self, speed_ms: int):
        self.speed_ms = speed_ms
        self.stop()
        self._tick()

    def validate(self) -> str:
        selected = self.items[(self.index - 1) % len(self.items)]
        return selected

    def _tick(self):
        self.on_highlight(self.index)
        self.index = (self.index + 1) % len(self.items)
        self._job = self._root.after(self.speed_ms, self._tick) 