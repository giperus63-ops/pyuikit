from ..widgets.frame import Frame


class FlowLayout:
    def __init__(self, app, master=None, gap=8, padding=0, min_width=None,
                 align="start", name=None):
        self.app = app
        self.gap = int(gap)
        if isinstance(padding, int):
            self.padding = (padding, padding, padding, padding)
        elif len(padding) == 2:
            self.padding = (padding[0], padding[1], padding[0], padding[1])
        else:
            self.padding = tuple(padding)
        self.min_width = min_width
        self.align = align
        self.name = name
        self._children = []
        self.container = Frame(app, master=master)
        self._last_width = 0
        self._rebuild()

    @property
    def tk(self):
        return self.container.tk

    def add(self, widget):
        self._children.append(widget)
        self._rebuild()
        return widget

    def remove(self, widget):
        if widget in self._children:
            self._children.remove(widget)
            widget.tk.pack_forget()
        self._rebuild()
        return self

    def clear(self):
        for widget in self._children:
            widget.tk.pack_forget()
        self._children.clear()
        return self

    def _wrap_width(self):
        width = self.container.tk.winfo_width()
        if width <= 1:
            return self.min_width or 600
        return width

    def _rebuild(self):
        pad_top, pad_right, pad_bottom, pad_left = self.padding
        self.container.tk.configure(padx=pad_left + pad_right, pady=pad_top + pad_bottom)
        wrap = self._wrap_width()
        self._last_width = wrap
        current_row_width = 0
        for widget in self._children:
            widget.tk.pack_forget()
        row_start = 0
        for widget in self._children:
            widget.tk.update_idletasks()
            w = widget.tk.winfo_reqwidth()
            if current_row_width + w > wrap and current_row_width > 0:
                self._pack_row(row_start, widget)
                row_start = self._children.index(widget)
                current_row_width = w + self.gap
            else:
                current_row_width += w + self.gap
        self._pack_row(row_start, None)
        return self

    def _pack_row(self, start, before):
        if before is not None:
            end = self._children.index(before)
        else:
            end = len(self._children)
        row_widgets = self._children[start:end]
        for widget in row_widgets:
            widget.tk.pack(side="left", padx=self.gap // 2, pady=self.gap // 2)