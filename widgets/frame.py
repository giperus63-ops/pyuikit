import tkinter as tk
from .base import Widget


class Frame(Widget):
    def __init__(self, app, variant="default", master=None, **kwargs):
        self.variant = variant
        style = app.style("frame", variant)
        super().__init__(app, master=master, style=style, **kwargs)

    def _build(self):
        self._tk = tk.Frame(self.master)
        style = self._resolve_style()
        self._apply_style(style)
        self._tk.configure(
            highlightthickness=style.border_width,
            highlightbackground=style.border.to_hex() if style.border else style.background.to_hex(),
        )
        self.app.register(self)

    def _apply_style(self, style):
        options = style.to_tk()
        options.pop("highlightbackground", None)
        if "bg" in options:
            options["bg"] = options["bg"]
        if options:
            try:
                self._tk.configure(**options)
            except tk.TclError:
                pass
        border_color = style.border.to_hex() if style.border else (style.background.to_hex() if style.background else None)
        if border_color is not None:
            try:
                self._tk.configure(highlightthickness=style.border_width,
                                   highlightbackground=border_color)
            except tk.TclError:
                pass