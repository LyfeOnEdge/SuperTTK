from tkinter import ttk


class button(ttk.Button):
    def __init__(self, frame, value, coords, callback):
        ttk.Button.__init__(
            self, frame, text=value, command=lambda: callback(self.value)
        )
        self.value = value
        self.coords = coords
        self.grid(column=coords[0], row=coords[1])


class base_keypad(ttk.Frame):
    def __init__(self, layout, callback, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.buttons = []
        for r in layout:
            for i in r:
                self.buttons.append(
                    button(self, i, (r.index(i), layout.index(r)), callback)
                )


##KEYPAD DEFINITIONS
TWELVE_KEY_LAYOUT = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"],
]


class twelve_button_keypad(base_keypad):
    def __init__(self, callback, *args, **kwargs):
        base_keypad.__init__(self, TWELVE_KEY_LAYOUT, callback, *args, **kwargs)
