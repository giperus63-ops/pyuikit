import unittest
from pyuikit.utils.color import Color
from pyuikit.utils.font import Font
from pyuikit.core.theme import Theme, ThemeRegistry
from pyuikit.core.style import Style


class TestColor(unittest.TestCase):
    def test_hex_short(self):
        c = Color("#abc")
        self.assertEqual(c.rgb, (0xaa, 0xbb, 0xcc))

    def test_hex_long(self):
        c = Color("#112233")
        self.assertEqual(c.rgb, (0x11, 0x22, 0x33))

    def test_named(self):
        c = Color("red")
        self.assertEqual(c.rgb, (255, 0, 0))

    def test_lighten_darken(self):
        c = Color("#808080")
        self.assertGreaterEqual(c.lighten(0.5).r, c.r)
        self.assertLessEqual(c.darken(0.5).r, c.r)

    def test_mix(self):
        a = Color("black")
        b = Color("white")
        m = a.mix(b, 0.5)
        self.assertEqual(m.rgb, (127, 127, 127))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            Color("not-a-color")


class TestFont(unittest.TestCase):
    def test_from_string(self):
        f = Font.from_string("Arial 14 bold")
        self.assertEqual(f.family, "Arial")
        self.assertEqual(f.size, 14)
        self.assertEqual(f.weight, "bold")

    def test_derive(self):
        f = Font(size=10)
        g = f.derive(size=20)
        self.assertEqual(g.size, 20)
        self.assertEqual(f.size, 10)

    def test_to_tuple(self):
        f = Font(family="Arial", size=12, weight="bold")
        self.assertEqual(f.to_tuple(), ("Arial", 12, "bold"))


class TestStyle(unittest.TestCase):
    def test_merged(self):
        a = Style(background="#000000", border_width=1)
        b = Style(foreground="#ffffff", radius=8)
        merged = a.merged(b)
        self.assertEqual(merged.background.to_hex(), "#000000")
        self.assertEqual(merged.foreground.to_hex(), "#ffffff")
        self.assertEqual(merged.radius, 8)
        self.assertEqual(merged.border_width, 1)

    def test_with_changes(self):
        s = Style(background="#000000")
        s2 = s.with_changes(background="#ffffff")
        self.assertEqual(s.background.to_hex(), "#000000")
        self.assertEqual(s2.background.to_hex(), "#ffffff")


class TestTheme(unittest.TestCase):
    def test_default_themes(self):
        self.assertTrue(ThemeRegistry.has("light"))
        self.assertTrue(ThemeRegistry.has("dark"))

    def test_merge(self):
        a = Theme(name="a", colors={"background": "#000000"})
        b = Theme(name="b", colors={"foreground": "#ffffff"})
        merged = a.merge(b)
        self.assertIn("background", merged.colors)
        self.assertIn("foreground", merged.colors)

    def test_color_lookup(self):
        theme = ThemeRegistry.get("light")
        self.assertEqual(theme.color("background").to_hex(), "#ffffff")


if __name__ == "__main__":
    unittest.main()