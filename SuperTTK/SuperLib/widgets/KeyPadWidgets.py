from tkinter import ttk


class KeypadButton(ttk.Button):
    """Base Keypad Button"""

    __desc__ = """Keypad button that automatically packs itself based on given coordinates. This object is not usually directly instantiated."""

    def __init__(self, frame, value, coords, callback):
        ttk.Button.__init__(
            self, frame, text=value, command=lambda: callback(self.value)
        )
        self.value = value
        self.coords = coords
        self.grid(column=coords[0], row=coords[1])


class BaseKeypad(ttk.Frame):
    """Base Keypad Class"""

    __desc__ = """Either instantiate directly with a custom layout or subclass with each subclass supplying a custom layout for more keypads. Subclass KeypadButton and supply the class as the "button_type" kwarg for custom buttons."""

    def __init__(self, layout, callback, button_class=KeypadButton, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.buttons = []
        for r in layout:
            for i in r:
                self.buttons.append(
                    button_class(self, i, (r.index(i), layout.index(r)), callback)
                )


class DialerKeypad(BaseKeypad):
    """Phone Dialer Keypad"""
    __desc__ = """Example 12-button keypad, subclass BaseKeypad and supply a custom layout for more keypads."""

    layout = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["*", "0", "#"],
    ]

    def __init__(self, callback, *args, **kwargs):
        base_keypad.__init__(self, self.layout, callback, *args, **kwargs)


KEYPAD_WIDGETS = [KeypadButton, BaseKeypad, DialerKeypad]
