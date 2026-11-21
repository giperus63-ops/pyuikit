import tkinter as tk
from tkinter import ttk
from .base import Widget


class Combobox(Widget):
    def __init__(self, app, values=None, variable=None, on_change=None,
                 variant="default", master=None, **kwargs):
        self.values = list(values or [])
        self.variable = variable if variable is not None else tk.StringVar()
        self.on_change = on_change
        self.variant = variant
        style = app.style("combobox", variant)
        super().__init__(app, master=master, style=style, **kwargs)
        self._tk.bind("<<ComboboxSelected>>", self._on_select, add="+")

    def _build(self):
        self._tk = ttk.Combobox(
            self.master,
            values=self.values,
            textvariable=self.variable,
            state="readonly",
        )
        style = self._resolve_style()
        if style.font is not None:
            self._tk.configure(font=style.font.to_tuple())
        self.app.register(self)

    def _on_select(self, _event):
        if callable(self.on_change):
            self.on_change(self.value)

    @property
    def value(self):
        return self.variable.get()

    def set_value(self, value):
        self.variable.set(value)
        return self

    def set_values(self, values):
        self.values = list(values)
        self._tk.configure(values=self.values)
        return self