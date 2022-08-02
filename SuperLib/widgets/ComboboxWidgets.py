import tkinter as tk
from tkinter import ttk
from .Labeler import Labeler
from .MultiWidget import MultiWidgetMixin


class LabeledCombobox(Labeler, ttk.Combobox):
    """Labeled Combobox widget"""

    __desc__ = """Set custom_values keyword to "False" to disable custom user-entered values. Set the "default" keyword to the index of the value to display by default from the "values" keyword."""

    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str,
        default: int = 0,
        custom_values: bool = True,
        values: list = (),
        is_child: bool = False,
        labelside: str = tk.LEFT,
    ):
        self.var = tk.StringVar()
        self.default = values[default] if any(values) else ""
        self.var.set(self.default)
        self.is_child = is_child
        Labeler.__init__(
            self, parent, labeltext, labelside=labelside, header=not is_child
        )
        ttk.Combobox.__init__(self, self.frame, textvariable=self.var)
        ttk.Combobox.pack(self, fill="x", expand=False, side=tk.TOP)
        self["values"] = values
        # Var to preserve custom values on enable / disable
        self._state = "normal" if custom_values else "readonly"

    def disable(self):
        """Disable Combobox. `Returns None`"""
        self["state"] = tk.DISABLED

    def enable(self):
        """Enable Combobox. `Returns None`"""
        self["state"] = self._state

    def get(self):
        """Get Combobox value. `Returns a String`"""
        return self.var.get()

    def set(self, val: str):
        """Set Combobox value. `Returns None`"""
        self.var.set(val)

    def clear(self):
        """Sets Combobox to its default value. `Returns None`"""
        self.var.set(self.default)


class LabeledMultiCombobox(Labeler, ttk.Frame, MultiWidgetMixin):
    """Labeled MultiWidget LabeledCombobox"""

    __desc__ = """Used when you need mutiple, vertically stacked Labeled Comboboxes"""

    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str,
        config: dict,
        is_child: bool = False,
        labelside=tk.TOP,
    ):
        Labeler.__init__(
            self, parent, labeltext, labelside=labelside, header=not is_child
        )
        ttk.Frame.__init__(self, self.frame)
        ttk.Frame.pack(self, fill=tk.BOTH, expand=True, side=tk.TOP)
        MultiWidgetMixin.__init__(self, LabeledCombobox, config)
        self.is_child = is_child


COMBOBOX_WIDGETS = [LabeledCombobox, LabeledMultiCombobox]
