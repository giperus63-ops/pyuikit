import re


class Color:
    _HEX_PATTERN = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

    def __init__(self, value):
        if isinstance(value, Color):
            self._r, self._g, self._b, self._a = value._r, value._g, value._b, value._a
            return
        if isinstance(value, tuple):
            parts = list(value)
            if len(parts) == 3:
                parts.append(1.0)
            if len(parts) != 4:
                raise ValueError("Tuple color must have 3 or 4 components")
            self._r, self._g, self._b, self._a = (
                int(parts[0]),
                int(parts[1]),
                int(parts[2]),
                float(parts[3]),
            )
            self._validate()
            return
        if isinstance(value, str):
            self._parse_string(value)
            return
        raise TypeError(f"Unsupported color type: {type(value)}")

    def _parse_string(self, value):
        name = value.strip().lower()
        named = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "red": (255, 0, 0),
            "green": (0, 128, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "gray": (128, 128, 128),
            "grey": (128, 128, 128),
            "orange": (255, 165, 0),
            "purple": (128, 0, 128),
            "transparent": (0, 0, 0, 0.0),
        }
        if name in named:
            parts = named[name]
            if len(parts) == 3:
                self._r, self._g, self._b = parts
                self._a = 1.0
            else:
                self._r, self._g, self._b, self._a = parts
            return
        match = self._HEX_PATTERN.match(name)
        if not match:
            raise ValueError(f"Invalid color string: {value}")
        hex_value = match.group(1)
        if len(hex_value) == 3:
            hex_value = "".join(ch * 2 for ch in hex_value)
        self._r = int(hex_value[0:2], 16)
        self._g = int(hex_value[2:4], 16)
        self._b = int(hex_value[4:6], 16)
        self._a = 1.0

    def _validate(self):
        for component in (self._r, self._g, self._b):
            if not 0 <= component <= 255:
                raise ValueError(f"RGB component out of range: {component}")
        if not 0.0 <= self._a <= 1.0:
            raise ValueError(f"Alpha out of range: {self._a}")

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b

    @property
    def a(self):
        return self._a

    @property
    def rgb(self):
        return (self._r, self._g, self._b)

    @property
    def rgba(self):
        return (self._r, self._g, self._b, self._a)

    def to_hex(self, with_alpha=False):
        base = f"#{self._r:02x}{self._g:02x}{self._b:02x}"
        if with_alpha:
            base += f"{int(self._a * 255):02x}"
        return base

    def lighten(self, amount=0.1):
        amount = max(0.0, min(1.0, amount))
        r = int(self._r + (255 - self._r) * amount)
        g = int(self._g + (255 - self._g) * amount)
        b = int(self._b + (255 - self._b) * amount)
        return Color((r, g, b, self._a))

    def darken(self, amount=0.1):
        amount = max(0.0, min(1.0, amount))
        r = int(self._r * (1.0 - amount))
        g = int(self._g * (1.0 - amount))
        b = int(self._b * (1.0 - amount))
        return Color((r, g, b, self._a))

    def mix(self, other, weight=0.5):
        other = Color(other)
        weight = max(0.0, min(1.0, weight))
        r = int(self._r * (1.0 - weight) + other._r * weight)
        g = int(self._g * (1.0 - weight) + other._g * weight)
        b = int(self._b * (1.0 - weight) + other._b * weight)
        a = self._a * (1.0 - weight) + other._a * weight
        return Color((r, g, b, a))

    def __eq__(self, other):
        try:
            other = Color(other)
        except (TypeError, ValueError):
            return NotImplemented
        return self.rgba == other.rgba

    def __hash__(self):
        return hash(self.rgba)

    def __repr__(self):
        return f"Color({self.to_hex()}, alpha={self._a})"