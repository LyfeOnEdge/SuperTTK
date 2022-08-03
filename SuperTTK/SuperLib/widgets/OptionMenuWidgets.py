#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from .Labeler import Labeler
from .MultiWidget import MultiWidgetMixin


class LabeledOptionMenu(Labeler, ttk.OptionMenu):
    """Labeled OptionMenu widget"""
    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str,
        options: list,
        default: int = 0,
        is_child: bool = False,
    ):
        self.var = tk.StringVar()
        self.is_child = is_child
        Labeler.__init__(self, parent, labeltext, header=not is_child)
        ttk.OptionMenu.__init__(self, self.frame, self.var, options[default], *options)
        ttk.OptionMenu.pack(self, fill="x", expand=False, side=tk.TOP)
        self.options = options
        self.default = default

    def enable(self):
        """Enable OptionMenu. `Returns None`"""
        self["state"] = tk.NORMAL

    def disable(self):
        """Disable OptionMenu. `Returns None`"""
        self["state"] = tk.DISABLED

    def get(self):
        """Get OptionMenu value. `Returns a String`"""
        return self.var.get()

    def set(self, val):
        """Set OptionMenu value. `Returns None`"""
        self.var.set(val)

    def clear(self):
        """Sets OptionMenu to its default value. `Returns None`"""
        self.var.set(self.options[self.default])


class LabeledMultiOptionMenu(Labeler, ttk.Frame, MultiWidgetMixin):
    """Labeled MultiWidget LabeledOptionMenu"""

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
        MultiWidgetMixin.__init__(self, LabeledOptionMenu, config)
        self.is_child = is_child


OPTIONMENU_WIDGETS = [LabeledOptionMenu, LabeledMultiOptionMenu]
