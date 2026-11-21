import tkinter as tk


class Transition:
    def __init__(self, widget, duration=200, steps=None, easing=None):
        self.widget = widget
        self.duration = int(duration)
        self.steps = steps if steps is not None else max(1, self.duration // 16)
        self.easing = easing or (lambda t: t)
        self._running = False

    def run(self, start, end, on_update, on_complete=None):
        if self._running:
            return self
        self._running = True
        target = self.widget.tk if hasattr(self.widget, "tk") else self.widget
        interval = max(1, self.duration // self.steps)

        def step(index):
            if index > self.steps:
                self._running = False
                if callable(on_complete):
                    on_complete()
                return
            t = index / self.steps
            eased = self.easing(t)
            value = start + (end - start) * eased
            try:
                on_update(value)
            except tk.TclError:
                self._running = False
                return
            target.after(interval, lambda: step(index + 1))

        on_update(start)
        target.after(interval, lambda: step(1))
        return self

    def cancel(self):
        self._running = False


def animate(widget, property_name, target_value, duration=200, steps=None,
            easing=None, on_complete=None):
    if not hasattr(widget, "tk"):
        raise TypeError("animate expects a Widget instance")

    def ease_out(t):
        return 1 - (1 - t) ** 3

    transition = Transition(widget, duration=duration, steps=steps, easing=easing or ease_out)

    target = widget.tk
    if property_name == "opacity":
        transition.run(1.0, float(target_value), lambda v: _apply_opacity(target, v),
                       on_complete=on_complete)
        return transition
    if property_name == "width":
        start = float(target.winfo_width())
        transition.run(start, float(target_value),
                       lambda v: target.configure(width=int(v)), on_complete=on_complete)
        return transition
    if property_name == "height":
        start = float(target.winfo_height())
        transition.run(start, float(target_value),
                       lambda v: target.configure(height=int(v)), on_complete=on_complete)
        return transition
    raise ValueError(f"Unsupported property for animation: {property_name}")


def _apply_opacity(target, value):
    try:
        alpha = max(0.0, min(1.0, value))
        target.wm_attributes("-alpha", alpha)
    except tk.TclError:
        pass