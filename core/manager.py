import tkinter as tk
from .theme import ThemeRegistry
from .style import Style
from ..utils.color import Color


class App:
    def __init__(self, title="PyUIKit App", theme="light", width=800, height=600,
                 resizable=(True, True), config=None):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(320, 240)
        self.root.resizable(resizable[0], resizable[1])
        self._theme = ThemeRegistry.get(theme)
        self._widgets = []
        self._style_cache = {}
        self._config = dict(config or {})
        self._apply_root_theme()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _apply_root_theme(self):
        bg = self._theme.color("background").to_hex()
        self.root.configure(bg=bg)

    @property
    def theme(self):
        return self._theme

    def set_theme(self, name_or_theme):
        if isinstance(name_or_theme, str):
            self._theme = ThemeRegistry.get(name_or_theme)
        else:
            self._theme = name_or_theme
        self._apply_root_theme()
        self._style_cache.clear()
        for widget in list(self._widgets):
            try:
                widget.refresh_style()
            except Exception:
                pass

    def register(self, widget):
        self._widgets.append(widget)

    def unregister(self, widget):
        if widget in self._widgets:
            self._widgets.remove(widget)

    def style(self, kind, variant="default"):
        key = (kind, variant)
        if key in self._style_cache:
            return self._style_cache[key].copy()
        builder = getattr(self, f"_style_{kind}_{variant}", None)
        if builder is None:
            builder = getattr(self, f"_style_{kind}", None)
        if builder is None:
            raise KeyError(f"No style builder for {kind}:{variant}")
        style = builder()
        self._style_cache[key] = style
        return style.copy()

    def _style_label_default(self):
        return Style(
            background=self._theme.color("background"),
            foreground=self._theme.color("text"),
            font=self._theme.font("body"),
        )

    def _style_label_heading(self):
        return Style(
            background=self._theme.color("background"),
            foreground=self._theme.color("text"),
            font=self._theme.font("heading"),
        )

    def _style_label_subheading(self):
        return Style(
            background=self._theme.color("background"),
            foreground=self._theme.color("text"),
            font=self._theme.font("subheading"),
        )

    def _style_label_muted(self):
        return Style(
            background=self._theme.color("background"),
            foreground=self._theme.color("text_muted"),
            font=self._theme.font("body"),
        )

    def _style_button_default(self):
        return Style(
            background=self._theme.color("surface"),
            foreground=self._theme.color("text"),
            border=self._theme.color("border"),
            border_width=1,
            radius=self._theme.radius("md"),
            padding=(self._theme.space("sm") + 2, self._theme.space("xs") + 2),
            font=self._theme.font("body"),
            cursor="hand2",
        )

    def _style_button_primary(self):
        return Style(
            background=self._theme.color("primary"),
            foreground=self._theme.color("primary_text"),
            border=None,
            border_width=0,
            radius=self._theme.radius("md"),
            padding=(self._theme.space("md"), self._theme.space("sm")),
            font=self._theme.font("body"),
            cursor="hand2",
        )

    def _style_button_danger(self):
        return Style(
            background=self._theme.color("danger"),
            foreground=self._theme.color("primary_text"),
            border=None,
            border_width=0,
            radius=self._theme.radius("md"),
            padding=(self._theme.space("md"), self._theme.space("sm")),
            font=self._theme.font("body"),
            cursor="hand2",
        )

    def _style_button_ghost(self):
        return Style(
            background=self._theme.color("background"),
            foreground=self._theme.color("text"),
            border=None,
            border_width=0,
            radius=self._theme.radius("md"),
            padding=(self._theme.space("sm"), self._theme.space("xs")),
            font=self._theme.font("body"),
            cursor="hand2",
        )

    def _style_entry_default(self):
        return Style(
            background=self._theme.color("input_bg"),
            foreground=self._theme.color("text"),
            border=self._theme.color("input_border"),
            border_width=1,
            radius=self._theme.radius("sm"),
            padding=(self._theme.space("sm"), self._theme.space("xs")),
            font=self._theme.font("body"),
        )

    def _style_frame_default(self):
        return Style(
            background=self._theme.color("background"),
            border=None,
            border_width=0,
            radius=0,
            padding=(0, 0),
        )

    def _style_frame_card(self):
        return Style(
            background=self._theme.color("surface"),
            border=self._theme.color("border"),
            border_width=1,
            radius=self._theme.radius("md"),
            padding=(self._theme.space("md"), self._theme.space("md")),
        )

    def _style_checkbox_default(self):
        return Style(
            background=self._theme.color("background"),
            foreground=self._theme.color("text"),
            font=self._theme.font("body"),
        )

    def _style_combobox_default(self):
        return Style(
            background=self._theme.color("input_bg"),
            foreground=self._theme.color("text"),
            border=self._theme.color("input_border"),
            border_width=1,
            radius=self._theme.radius("sm"),
            font=self._theme.font("body"),
        )

    def run(self):
        self.root.mainloop()

    def close(self):
        for widget in list(self._widgets):
            try:
                widget.destroy()
            except Exception:
                pass
        self._widgets.clear()
        self.root.destroy()

    def after(self, ms, callback):
        return self.root.after(ms, callback)

    def config_value(self, key, default=None):
        return self._config.get(key, default)