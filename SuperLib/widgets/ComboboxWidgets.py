import tkinter as tk
from tkinter import ttk
from .Labeler import Labeler
from .MultiWidget import MultiWidgetMixin
from .WidgetsCore import SuperWidgetMixin
from typing import Callable

class LabeledCombobox(Labeler, ttk.Combobox, SuperWidgetMixin):
    """Labeled Combobox with the Super Widget mixin"""

    __desc__ = """Set custom_values keyword to "False" to disable custom user-entered values. Set the "default" keyword to the index of the value to display by default from the "values" keyword."""

    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str,
        command: Callable = None,
        default: int = 0,
        on_keystroke: bool = False,
        bind_enter: bool = True,
        bind_escape_clear: bool = True,
        values: list = (),
        custom_values: bool = True,
        labelside: str = tk.LEFT,
        is_child: bool = False,
        min_width: int = 0,
        widgetargs={},
        **kw
    ):
        self.var = tk.StringVar()
        self.default = values[default] if any(values) else ""
        self.var.set(self.default)
        Labeler.__init__(self, parent, labeltext, labelside=labelside, header=not is_child)
        ttk.Combobox.__init__(
            self, self.frame, textvariable=self.var, **kw
        )
        ttk.Combobox.pack(self, fill=tk.BOTH, expand=True, side=tk.TOP)
        SuperWidgetMixin.__init__(self, **widgetargs)

        self.is_child = is_child
        
        self["values"] = values
        self._state = "normal" if custom_values else "readonly"
        self._command = command
        if on_keystroke:
            self.bind("<KeyRelease>", self._on_execute_command)
        if bind_enter:
            self.bind("<Return>", self._on_execute_command)
        if bind_escape_clear:
            self.bind("<Escape>", self.clear())

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

    def _on_execute_command(self, event=None):
        """Calls the provided "command" function with the contents of the Entry. `Returns None`"""
        if self._command:
            self._command(self.get())


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
