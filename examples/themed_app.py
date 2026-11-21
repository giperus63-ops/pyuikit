from pyuikit import App, Label, Button, StackLayout, Frame, Theme, ThemeRegistry

def main():
    custom = Theme(
        name="ocean",
        colors={
            "background": "#0b1d2a",
            "surface": "#123447",
            "surface_alt": "#1a4a63",
            "text": "#e6f5ff",
            "text_muted": "#8fbcd4",
            "border": "#1f5a77",
            "primary": "#00a8e8",
            "primary_hover": "#22bdf7",
            "primary_active": "#0087ba",
            "primary_text": "#ffffff",
            "input_bg": "#0f2b3b",
            "input_border": "#1f5a77",
            "input_focus": "#00a8e8",
            "danger": "#ef476f",
            "danger_hover": "#f96c8e",
            "success": "#06d6a0",
            "warning": "#ffd166",
        },
    )
    ThemeRegistry.register(custom)
    app = App(title="PyUIKit Themed Example", theme="ocean", width=560, height=460)
    layout = StackLayout(app, direction="vertical", gap=14, padding=24)
    layout.tk.pack(fill="both", expand=True)
    layout.add(Label(app, "Ocean Theme", variant="heading"))
    layout.add(Label(app, "Custom themes can be registered and switched at runtime",
                     variant="muted"))
    card = Frame(app, variant="card")
    card_layout = StackLayout(app, master=card, direction="vertical", gap=8, padding=12)
    card_layout.tk.pack(fill="both", expand=True)
    card_layout.add(Label(app, "Current theme: ocean"))
    card_layout.add(Label(app, "Try switching between light, dark and ocean", variant="muted"))
    layout.add(card, fill="x")
    buttons = StackLayout(app, direction="horizontal", gap=8)
    buttons.tk.pack(fill="x")
    status = Label(app, "Theme: ocean", variant="muted")

    def switch(name):
        app.set_theme(name)
        status.set_text(f"Theme: {name}")
    buttons.add(Button(app, "Light", on_click=lambda: switch("light"), variant="default"))
    buttons.add(Button(app, "Dark", on_click=lambda: switch("dark"), variant="default"))
    buttons.add(Button(app, "Ocean", on_click=lambda: switch("ocean"), variant="primary"))
    layout.add(buttons.tk)
    layout.add(status)
    app.run()

if __name__ == "__main__":
    main()