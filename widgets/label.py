import tkinter as tk
from .base import Widget


class Label(Widget):
    def __init__(self, app, text="", variant="default", master=None, **kwargs):
        self.text = text
        self.variant = variant
        style = app.style("label", variant)
        super().__init__(app, master=master, style=style, **kwargs)

    def _build(self):
        self._tk = tk.Label(self.master, text=self.text)
        self._apply_style(self._resolve_style())
        self.app.register(self)

    def set_text(self, text):
        self.text = text
        self._tk.configure(text=text)
        return self