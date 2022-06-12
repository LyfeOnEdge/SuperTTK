#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from typing import Callable
from .Labeler import Labeler
from .Scroller import Scroller, _create_container
from .WidgetsCore import default_pack
from .EntryWidgets import LabeledButtonEntry
from .TextWidgets import ScrolledText


class ConsoleWidget(Labeler, ttk.Frame):
    """Set labeltext, even if temporarily at init or the label widget will be ignored"""

    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str = "Console: ",
        entrylabeltext: str = "Command: ",
        labelside=tk.TOP,
        buttontext: str = "Run",
        is_child=False,
        **kwargs
    ):
        self.is_child = is_child
        self.command = kwargs.get("command")
        if labeltext:  # If no label at
            Labeler.__init__(
                self, parent, labeltext, labelside=labelside, header=not is_child
            )
            ttk.Frame.__init__(self, self.frame)
            ttk.Frame.pack(self, fill="both", expand=True, side=tk.TOP)
        else:
            ttk.Frame.__init__(self, parent)
        self.console = ScrolledText(
            self,
            textkw={"highlightthickness": 0, "state": tk.DISABLED},
        )
        self.console.pack(fill="both", expand=True, side=tk.TOP)
        self.entry = LabeledButtonEntry(
            self,
            labeltext=entrylabeltext,
            buttontext=buttontext,
            command=self._on_command,
            **kwargs
        )
        self.entry.pack(fill="x", expand=False, side=tk.TOP)

    def _on_command(self, event=None):
        if self.command:
            self.command(self.entry.get().strip())
        self.entry.clear()

    def print(self, val):
        self.console.configure(state=tk.NORMAL)
        self.console.insert(tk.END, val + "\n")
        self.console.configure(state=tk.DISABLED)
