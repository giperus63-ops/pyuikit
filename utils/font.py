from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Font:
    family: str = "TkDefaultFont"
    size: int = 12
    weight: str = "normal"
    slant: str = "roman"
    underline: bool = False
    overstrike: bool = False

    def __post_init__(self):
        if self.size <= 0:
            raise ValueError("Font size must be positive")
        if self.weight not in ("normal", "bold"):
            raise ValueError("weight must be 'normal' or 'bold'")
        if self.slant not in ("roman", "italic"):
            raise ValueError("slant must be 'roman' or 'italic'")

    def to_tuple(self):
        style_bits = []
        if self.weight == "bold":
            style_bits.append("bold")
        if self.slant == "italic":
            style_bits.append("italic")
        if self.underline:
            style_bits.append("underline")
        if self.overstrike:
            style_bits.append("overstrike")
        return (self.family, self.size, " ".join(style_bits) if style_bits else "normal")

    def derive(self, **kwargs):
        data = {
            "family": self.family,
            "size": self.size,
            "weight": self.weight,
            "slant": self.slant,
            "underline": self.underline,
            "overstrike": self.overstrike,
        }
        data.update(kwargs)
        return Font(**data)

    @classmethod
    def from_string(cls, spec: str) -> Optional["Font"]:
        if not spec:
            return None
        parts = spec.split()
        family = parts[0]
        size = 12
        weight = "normal"
        slant = "roman"
        for part in parts[1:]:
            if part.isdigit() or (part.startswith("-") and part[1:].isdigit()):
                size = abs(int(part))
            elif part.lower() == "bold":
                weight = "bold"
            elif part.lower() == "italic":
                slant = "italic"
        return cls(family=family, size=size, weight=weight, slant=slant)