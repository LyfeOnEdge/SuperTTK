#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from .Labeler import Labeler
from .MultiWidget import MultiWidgetMixin


class LabeledCheckbutton(Labeler, ttk.Checkbutton):
    """Labeled Checkbutton"""

    __desc__ = """The "replace_output" keyword argument allows the user to \
provide a tuple of len 2 to replace the default True/False return values. \
The "is_child" keyword is used by the multiwidget mixin for label \
configuration and should probably be left alone unless you are making your \
own multiwidgets."""

    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str = "",
        replace_output: list = None,
        default: bool = False,
        is_child: bool = False,
        **kw,
    ):
        self.var = tk.IntVar()
        self.default = default
        self.var.set(default)
        self.replace_output = replace_output
        self.is_child = is_child
        Labeler.__init__(self, parent, labeltext, header=not is_child)
        ttk.Checkbutton.__init__(self, self.frame, variable=self.var, **kw)
        ttk.Checkbutton.pack(self, fill="x", expand=False, side=tk.TOP)

    def enable(self):
        """Enable Checkbutton. `Returns None`"""
        self["state"] = tk.NORMAL

    def disable(self):
        """Disable Checkbutton. `Returns None`"""
        self["state"] = tk.DISABLED

    def get(self):
        """Get Checkbutton value. `Returns a Boolean unless replace_output is set`"""
        v = self.var.get()
        return self.replace_output[v] if self.replace_output else v

    def set(self, val: bool):
        """Set Checkbutton value. `Returns None`"""
        self.var.set(val)

    def clear(self):
        """Sets the Checkbutton to its default value, usually *False* `Returns None`"""
        self.var.set(self.default)


class LabeledMultiCheckbutton(Labeler, ttk.Frame, MultiWidgetMixin):
    """Labeled MultiWidget LabeledCheckbutton."""

    __desc__ = (
        """Used when you need multiple, vertically stacked Labeled Checkbuttons"""
    )

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
        MultiWidgetMixin.__init__(self, LabeledCheckbutton, config)
        self.is_child = is_child


CHECKBUTTON_WIDGETS = [LabeledCheckbutton, LabeledMultiCheckbutton]
