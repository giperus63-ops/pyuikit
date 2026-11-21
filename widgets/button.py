import tkinter as tk

from .base import Widget


class Button(Widget):
    def __init__(self, app, text="", on_click=None, variant="default", master=None, **kwargs):
        self.text = text
        self.on_click = on_click
        self.variant = variant
        self._hover = False
        self._pressed = False
        style = app.style("button", variant)
        super().__init__(app, master=master, style=style, **kwargs)
        self._bind_events()

    def _build(self):
        self._tk = tk.Button(self.master, text=self.text, relief="flat", borderwidth=0,
                             highlightthickness=0, command=self._handle_click)
        self._apply_style(self._resolve_style())
        self.app.register(self)

    def _bind_events(self):
        self._tk.bind("<Enter>", self._on_enter, add="+")
        self._tk.bind("<Leave>", self._on_leave, add="+")
        self._tk.bind("<ButtonPress-1>", self._on_press, add="+")
        self._tk.bind("<ButtonRelease-1>", self._on_release, add="+")

    def _handle_click(self):
        if callable(self.on_click):
            self.on_click()

    def _hover_color(self, style):
        theme = self.app.theme
        if self.variant == "primary":
            return theme.color("primary_hover")
        if self.variant == "danger":
            return theme.color("danger_hover")
        if self.variant == "ghost":
            return theme.color("surface")
        return theme.color("surface_alt")

    def _active_color(self, style):
        theme = self.app.theme
        if self.variant == "primary":
            return theme.color("primary_active")
        if self.variant == "danger":
            return theme.color("danger")
        if self.variant == "ghost":
            return theme.color("surface_alt")
        return theme.color("border")

    def _on_enter(self, _event):
        self._hover = True
        self._refresh_state()

    def _on_leave(self, _event):
        self._hover = False
        self._pressed = False
        self._refresh_state()

    def _on_press(self, _event):
        self._pressed = True
        self._refresh_state()

    def _on_release(self, _event):
        self._pressed = False
        self._refresh_state()

    def _refresh_state(self):
        style = self._resolve_style()
        if self._pressed:
            style = style.with_changes(background=self._active_color(style))
        elif self._hover:
            style = style.with_changes(background=self._hover_color(style))
        self._apply_style(style)

    def set_text(self, text):
        self.text = text
        self._tk.configure(text=text)
        return self

    def set_on_click(self, callback):
        self.on_click = callback
        return self

    def enable(self):
        self._tk.configure(state="normal")
        return self

    def disable(self):
        self._tk.configure(state="disabled")
        return self