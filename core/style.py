from copy import deepcopy
from ..utils.color import Color
from ..utils.font import Font


class Style:
    def __init__(self, background=None, foreground=None, border=None, border_width=0,
                 radius=0, padding=(0, 0), font=None, cursor=None, opacity=None,
                 width=None, height=None):
        self.background = Color(background) if background is not None else None
        self.foreground = Color(foreground) if foreground is not None else None
        self.border = Color(border) if border is not None else None
        self.border_width = int(border_width)
        self.radius = int(radius)
        if isinstance(padding, int):
            self.padding = (padding, padding)
        else:
            self.padding = tuple(padding)
        self.font = font if isinstance(font, Font) or font is None else Font.from_string(font)
        self.cursor = cursor
        self.opacity = opacity
        self.width = width
        self.height = height

    def copy(self):
        return deepcopy(self)

    def with_changes(self, **kwargs):
        new = self.copy()
        for key, value in kwargs.items():
            if not hasattr(new, key):
                raise AttributeError(f"Unknown style attribute: {key}")
            if key in ("background", "foreground", "border") and value is not None:
                value = Color(value)
            if key == "font" and isinstance(value, str):
                value = Font.from_string(value)
            setattr(new, key, value)
        return new

    def merged(self, other):
        if other is None:
            return self.copy()
        if not isinstance(other, Style):
            raise TypeError("Can only merge with another Style")
        result = self.copy()
        for attr in ("background", "foreground", "border", "font", "cursor",
                     "opacity", "width", "height"):
            value = getattr(other, attr)
            if value is not None:
                setattr(result, attr, value)
        if other.border_width:
            result.border_width = other.border_width
        if other.radius:
            result.radius = other.radius
        if other.padding != (0, 0):
            result.padding = other.padding
        return result

    def to_dict(self):
        return {
            "background": self.background.to_hex(with_alpha=True) if self.background else None,
            "foreground": self.foreground.to_hex(with_alpha=True) if self.foreground else None,
            "border": self.border.to_hex(with_alpha=True) if self.border else None,
            "border_width": self.border_width,
            "radius": self.radius,
            "padding": self.padding,
            "font": self.font.to_tuple() if self.font else None,
            "cursor": self.cursor,
            "opacity": self.opacity,
            "width": self.width,
            "height": self.height,
        }

    def to_tk(self):
        options = {}
        if self.background is not None:
            options["bg"] = self.background.to_hex()
        if self.foreground is not None:
            options["fg"] = self.foreground.to_hex()
        if self.font is not None:
            options["font"] = self.font.to_tuple()
        if self.cursor is not None:
            options["cursor"] = self.cursor
        if self.width is not None:
            options["width"] = self.width
        if self.height is not None:
            options["height"] = self.height
        return options

    def __repr__(self):
        return f"Style({self.to_dict()})"