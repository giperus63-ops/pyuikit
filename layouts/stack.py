import tkinter as tk
from ..widgets.frame import Frame


class StackLayout:
    def __init__(self, app, master=None, direction="vertical", gap=8, padding=0,
                 align="start", name=None):
        self.app = app
        self.direction = direction
        self.gap = int(gap)
        if isinstance(padding, int):
            self.padding = (padding, padding, padding, padding)
        elif len(padding) == 2:
            self.padding = (padding[0], padding[1], padding[0], padding[1])
        else:
            self.padding = tuple(padding)
        self.align = align
        self.name = name
        self._children = []
        self.container = Frame(app, master=master)
        self.container.tk.pack_propagate(False)
        self._outer = self.container.tk
        self._rebuild()

    @property
    def tk(self):
        return self.container.tk

    def add(self, widget, expand=False, fill=None):
        self._children.append({"widget": widget, "expand": expand, "fill": fill})
        self._rebuild()
        return widget

    def remove(self, widget):
        for entry in list(self._children):
            if entry["widget"] is widget:
                self._children.remove(entry)
                widget.tk.pack_forget()
                break
        self._rebuild()
        return self

    def clear(self):
        for entry in list(self._children):
            entry["widget"].tk.pack_forget()
        self._children.clear()
        return self

    def _rebuild(self):
        pad_top, pad_right, pad_bottom, pad_left = self.padding
        self._outer.configure(padx=pad_left + pad_right, pady=pad_top + pad_bottom)
        for entry in self._children:
            entry["widget"].tk.pack_forget()
        for index, entry in enumerate(self._children):
            widget = entry["widget"]
            is_last = index == len(self._children) - 1
            expand = entry["expand"]
            fill = entry["fill"]
            if self.direction == "vertical":
                side = "top"
                if fill is None:
                    fill = "x" if self.align == "stretch" else None
                padx = 0
                pady = (0, 0 if is_last else self.gap)
                anchor = None
                if self.align == "start":
                    anchor = "w"
                elif self.align == "end":
                    anchor = "e"
                elif self.align == "center":
                    anchor = "center"
                widget.tk.pack(side=side, fill=fill, expand=expand,
                               padx=padx, pady=pady, anchor=anchor) if anchor else \
                    widget.tk.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady)
            else:
                side = "left"
                if fill is None:
                    fill = "y" if self.align == "stretch" else None
                padx = (0, 0 if is_last else self.gap)
                pady = 0
                anchor = None
                if self.align == "start":
                    anchor = "n"
                elif self.align == "end":
                    anchor = "s"
                elif self.align == "center":
                    anchor = "center"
                widget.tk.pack(side=side, fill=fill, expand=expand,
                               padx=padx, pady=pady, anchor=anchor) if anchor else \
                    widget.tk.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady)
        return self