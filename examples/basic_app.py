from pyuikit import App, Label, Button, Entry, StackLayout, Frame, Checkbox


def main():
    app = App(title="PyUIKit Basic Example", theme="light", width=520, height=420)
    root_layout = StackLayout(app, direction="vertical", gap=12, padding=20)
    root_layout.tk.pack(fill="both", expand=True)
    title = Label(app, "Welcome to PyUIKit", variant="heading")
    subtitle = Label(app, "A simple demo of widgets and layouts", variant="muted")
    root_layout.add(title)
    root_layout.add(subtitle)
    card = Frame(app, variant="card")
    card_layout = StackLayout(app, master=card, direction="vertical", gap=10, padding=12)
    card_layout.tk.pack(fill="both", expand=True)
    name_label = Label(app, "Your name")
    name_entry = Entry(app, placeholder="Enter your name")
    card_layout.add(name_label)
    card_layout.add(name_entry)
    remember = Checkbox(app, text="Remember me")
    card_layout.add(remember)
    root_layout.add(card, fill="x")
    actions = StackLayout(app, direction="horizontal", gap=8)
    actions.tk.pack(fill="x", pady=(8, 0))
    status = Label(app, "Ready", variant="muted")

    def on_submit():
        name = name_entry.value or "stranger"
        remember_text = " (remembered)" if remember.value else ""
        status.set_text(f"Hello, {name}{remember_text}!")
    submit = Button(app, "Submit", on_click=on_submit, variant="primary")
    reset = Button(app, "Reset", on_click=lambda: (name_entry.clear(), remember.set_value(False), status.set_text("Ready")))
    actions.add(submit)
    actions.add(reset)
    root_layout.add(actions.tk)
    root_layout.add(status)
    app.run()

if __name__ == "__main__":
    main()