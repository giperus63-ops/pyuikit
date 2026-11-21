import tkinter as tk

from ..core.style import Style


class Widget:
    def __init__(self, app, master=None, style=None, style_overrides=None,
                 name=None, **style_kwargs):
        self.app = app
        self.master = master if master is not None else app.root
        self.name = name
        self._tk = None
        self._style = style
        self._style_overrides = style_overrides
        self._style_kwargs = style_kwargs
        self._build()

    def _build(self):
        raise NotImplementedError

    def _resolve_style(self):
        base = self._style.copy() if isinstance(self._style, Style) else None
        if self._style_overrides is not None:
            if base is None:
                base = self._style_overrides.copy()
            else:
                base = base.merged(self._style_overrides)
        if base is None:
            base = Style()
        if self._style_kwargs:
            base = base.with_changes(**self._style_kwargs)
        return base

    @property
    def tk(self):
        return self._tk

    @property
    def style(self):
        return self._resolve_style()

    def apply_style(self, style):
        self._style = style
        self.refresh_style()

    def refresh_style(self):
        if self._tk is not None:
            self._apply_style(self._resolve_style())

    def _apply_style(self, style):
        options = style.to_tk()
        if options:
            try:
                self._tk.configure(**options)
            except tk.TclError:
                pass

    def pack(self, **kwargs):
        self._tk.pack(**kwargs)
        return self

    def grid(self, **kwargs):
        self._tk.grid(**kwargs)
        return self

    def place(self, **kwargs):
        self._tk.place(**kwargs)
        return self

    def pack_forget(self):
        self._tk.pack_forget()
        return self

    def grid_forget(self):
        self._tk.grid_forget()
        return self

    def place_forget(self):
        self._tk.place_forget()
        return self

    def destroy(self):
        self.app.unregister(self)
        if self._tk is not None:
            try:
                self._tk.destroy()
            except tk.TclError:
                pass
            self._tk = None