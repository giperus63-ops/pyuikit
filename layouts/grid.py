from ..widgets.frame import Frame


class GridLayout:
    def __init__(self, app, master=None, columns=2, gap=8, padding=0, name=None):
        self.app = app
        self.columns = int(columns)
        self.gap = int(gap)
        if isinstance(padding, int):
            self.padding = (padding, padding, padding, padding)
        elif len(padding) == 2:
            self.padding = (padding[0], padding[1], padding[0], padding[1])
        else:
            self.padding = tuple(padding)
        self.name = name
        self._children = []
        self.container = Frame(app, master=master)
        self._rebuild()

    @property
    def tk(self):
        return self.container.tk

    def add(self, widget, row=None, column=None, rowspan=1, columnspan=1,
            sticky="nsew", expand=False):
        entry = {
            "widget": widget,
            "row": row,
            "column": column,
            "rowspan": rowspan,
            "columnspan": columnspan,
            "sticky": sticky,
            "expand": expand,
        }
        self._children.append(entry)
        self._rebuild()
        return widget

    def remove(self, widget):
        for entry in list(self._children):
            if entry["widget"] is widget:
                entry["widget"].tk.grid_forget()
                self._children.remove(entry)
                break
        self._rebuild()
        return self

    def clear(self):
        for entry in list(self._children):
            entry["widget"].tk.grid_forget()
        self._children.clear()
        return self

    def _rebuild(self):
        pad_top, pad_right, pad_bottom, pad_left = self.padding
        container_tk = self.container.tk
        container_tk.configure(padx=pad_left + pad_right, pady=pad_top + pad_bottom)
        for index in range(self.columns):
            container_tk.grid_columnconfigure(index, weight=1)
        col = 0
        row = 0
        for entry in self._children:
            widget = entry["widget"]
            widget.tk.grid_forget()
            if entry["row"] is None:
                entry["row"] = row
            if entry["column"] is None:
                entry["column"] = col
            widget.tk.grid(
                row=entry["row"],
                column=entry["column"],
                rowspan=entry["rowspan"],
                columnspan=entry["columnspan"],
                sticky=entry["sticky"],
                padx=self.gap // 2,
                pady=self.gap // 2,
            )
            if entry["expand"]:
                container_tk.grid_rowconfigure(entry["row"], weight=1)
            col += entry["columnspan"]
            if col >= self.columns:
                col = 0
                row += 1
        return self