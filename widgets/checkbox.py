import tkinter as tk
from .base import Widget


class Checkbox(Widget):
    def __init__(self, app, text="", variable=None, command=None, variant="default",
                 master=None, **kwargs):
        self.text = text
        self.variable = variable if variable is not None else tk.BooleanVar(value=False)
        self.command = command
        self.variant = variant
        style = app.style("checkbox", variant)
        super().__init__(app, master=master, style=style, **kwargs)

    def _build(self):
        self._tk = tk.Checkbutton(
            self.master,
            text=self.text,
            variable=self.variable,
            command=self._on_toggle,
            anchor="w",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
        )
        self._apply_style(self._resolve_style())
        self.app.register(self)

    def _on_toggle(self):
        if callable(self.command):
            self.command(self.value)

    @property
    def value(self):
        return bool(self.variable.get())

    def set_value(self, value):
        self.variable.set(bool(value))
        return self

    def set_text(self, text):
        self.text = text
        self._tk.configure(text=text)
        return self