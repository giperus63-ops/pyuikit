from ..utils.color import Color
from ..utils.font import Font


class Theme:
    def __init__(self, name, colors=None, fonts=None, spacing=None, radii=None):
        self.name = name
        self.colors = dict(colors or {})
        self.fonts = dict(fonts or {})
        self.spacing = dict(spacing or {})
        self.radii = dict(radii or {})
        self._normalize()

    def _normalize(self):
        for key, value in list(self.colors.items()):
            if not isinstance(value, Color):
                self.colors[key] = Color(value)
        for key, value in list(self.fonts.items()):
            if isinstance(value, str):
                parsed = Font.from_string(value)
                if parsed is not None:
                    self.fonts[key] = parsed

    def color(self, key, default=None):
        if key in self.colors:
            return self.colors[key]
        if default is not None:
            return Color(default)
        raise KeyError(f"Unknown color key: {key}")

    def font(self, key, default=None):
        if key in self.fonts:
            return self.fonts[key]
        return default

    def space(self, key, default=0):
        return self.spacing.get(key, default)

    def radius(self, key, default=0):
        return self.radii.get(key, default)

    def merge(self, other):
        if not isinstance(other, Theme):
            raise TypeError("Can only merge with another Theme")
        merged_colors = dict(self.colors)
        merged_colors.update(other.colors)
        merged_fonts = dict(self.fonts)
        merged_fonts.update(other.fonts)
        merged_spacing = dict(self.spacing)
        merged_spacing.update(other.spacing)
        merged_radii = dict(self.radii)
        merged_radii.update(other.radii)
        return Theme(
            name=f"{self.name}+{other.name}",
            colors=merged_colors,
            fonts=merged_fonts,
            spacing=merged_spacing,
            radii=merged_radii,
        )

    def with_overrides(self, colors=None, fonts=None, spacing=None, radii=None):
        merged_colors = dict(self.colors)
        merged_colors.update(colors or {})
        merged_fonts = dict(self.fonts)
        merged_fonts.update(fonts or {})
        merged_spacing = dict(self.spacing)
        merged_spacing.update(spacing or {})
        merged_radii = dict(self.radii)
        merged_radii.update(radii or {})
        return Theme(
            name=self.name,
            colors=merged_colors,
            fonts=merged_fonts,
            spacing=merged_spacing,
            radii=merged_radii,
        )

    def to_dict(self):
        return {
            "name": self.name,
            "colors": {k: v.to_hex() for k, v in self.colors.items()},
            "fonts": {k: v.to_tuple() for k, v in self.fonts.items()},
            "spacing": dict(self.spacing),
            "radii": dict(self.radii),
        }


class ThemeRegistry:
    _themes = {}

    @classmethod
    def register(cls, theme):
        if not isinstance(theme, Theme):
            raise TypeError("Can only register Theme instances")
        cls._themes[theme.name] = theme

    @classmethod
    def get(cls, name):
        if name not in cls._themes:
            raise KeyError(f"Theme not registered: {name}")
        return cls._themes[name]

    @classmethod
    def has(cls, name):
        return name in cls._themes

    @classmethod
    def all(cls):
        return dict(cls._themes)

    @classmethod
    def unregister(cls, name):
        cls._themes.pop(name, None)


def _build_default_themes():
    light = Theme(
        name="light",
        colors={
            "background": "#ffffff",
            "surface": "#f5f5f5",
            "surface_alt": "#e8e8e8",
            "text": "#1a1a1a",
            "text_muted": "#666666",
            "border": "#d0d0d0",
            "primary": "#2d6cdf",
            "primary_hover": "#4a83e8",
            "primary_active": "#1f56b8",
            "primary_text": "#ffffff",
            "success": "#2ea44f",
            "warning": "#d9822b",
            "danger": "#d73a49",
            "danger_hover": "#e05c6a",
            "input_bg": "#ffffff",
            "input_border": "#c8c8c8",
            "input_focus": "#2d6cdf",
            "shadow": "#00000033",
        },
        fonts={
            "body": Font(family="Segoe UI", size=11),
            "heading": Font(family="Segoe UI", size=20, weight="bold"),
            "subheading": Font(family="Segoe UI", size=15, weight="bold"),
            "caption": Font(family="Segoe UI", size=9),
            "code": Font(family="Consolas", size=11),
        },
        spacing={
            "xs": 4,
            "sm": 8,
            "md": 12,
            "lg": 20,
            "xl": 32,
        },
        radii={
            "sm": 4,
            "md": 8,
            "lg": 14,
            "pill": 999,
        },
    )
    dark = Theme(
        name="dark",
        colors={
            "background": "#1e1e2e",
            "surface": "#2a2a3c",
            "surface_alt": "#33334a",
            "text": "#f0f0f5",
            "text_muted": "#a0a0b8",
            "border": "#40405a",
            "primary": "#5b8def",
            "primary_hover": "#7aa3f5",
            "primary_active": "#3f6ed1",
            "primary_text": "#ffffff",
            "success": "#3fb950",
            "warning": "#e3b341",
            "danger": "#f85149",
            "danger_hover": "#ff6b63",
            "input_bg": "#252538",
            "input_border": "#484862",
            "input_focus": "#5b8def",
            "shadow": "#00000066",
        },
        fonts={
            "body": Font(family="Segoe UI", size=11),
            "heading": Font(family="Segoe UI", size=20, weight="bold"),
            "subheading": Font(family="Segoe UI", size=15, weight="bold"),
            "caption": Font(family="Segoe UI", size=9),
            "code": Font(family="Consolas", size=11),
        },
        spacing={
            "xs": 4,
            "sm": 8,
            "md": 12,
            "lg": 20,
            "xl": 32,
        },
        radii={
            "sm": 4,
            "md": 8,
            "lg": 14,
            "pill": 999,
        },
    )
    ThemeRegistry.register(light)
    ThemeRegistry.register(dark)

_build_default_themes()