import tkinter as tk
from .base import Widget


class Entry(Widget):
    def __init__(self, app, textvariable=None, placeholder="", variant="default",
                 master=None, **kwargs):
        self.variable = textvariable if textvariable is not None else tk.StringVar()
        self.placeholder = placeholder
        self.variant = variant
        self._showing_placeholder = False
        style = app.style("entry", variant)
        super().__init__(app, master=master, style=style, **kwargs)
        self._bind_placeholder()

    def _build(self):
        self._tk = tk.Entry(self.master, textvariable=self.variable, relief="flat",
                            borderwidth=0, highlightthickness=1)
        style = self._resolve_style()
        self._apply_style(style)
        if style.border is not None:
            self._tk.configure(highlightbackground=style.border.to_hex(),
                               highlightcolor=self.app.theme.color("input_focus").to_hex())
        self.app.register(self)
        if self.placeholder and not self.variable.get():
            self._show_placeholder()

    def _bind_placeholder(self):
        self._tk.bind("<FocusIn>", self._on_focus_in, add="+")
        self._tk.bind("<FocusOut>", self._on_focus_out, add="+")

    def _show_placeholder(self):
        if not self.placeholder:
            return
        self._showing_placeholder = True
        self.variable.set(self.placeholder)
        self._tk.configure(fg=self.app.theme.color("text_muted").to_hex())

    def _hide_placeholder(self):
        if not self.placeholder:
            return
        self._showing_placeholder = False
        self.variable.set("")
        self._tk.configure(fg=self.app.theme.color("text").to_hex())

    def _on_focus_in(self, _event):
        if self._showing_placeholder:
            self._hide_placeholder()

    def _on_focus_out(self, _event):
        if self.placeholder and not self.variable.get():
            self._show_placeholder()

    @property
    def value(self):
        if self._showing_placeholder:
            return ""
        return self.variable.get()

    def set_value(self, value):
        if self._showing_placeholder:
            self._hide_placeholder()
        self.variable.set(value)
        return self

    def clear(self):
        self.set_value("")
        if self.placeholder:
            self._show_placeholder()
        return self