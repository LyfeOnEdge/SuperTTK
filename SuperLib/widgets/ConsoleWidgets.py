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

    __desc__ = """Used when you need to drop a console interface into an application. \
To write to the console call console.print(value). Pass a function as the "command" \
keyword argument to handle the entry input."""

    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str = "Console: ",
        entrylabeltext: str = "Command: ",
        labelside: str = tk.TOP,
        button_text: str = "Run",
        is_child: bool = False,
        **kwargs
    ):
        self.is_child = is_child
        self.command = kwargs.get("command")
        if labeltext:  # If no label at init the label is never inited
            Labeler.__init__(
                self, parent, labeltext, labelside=labelside, header=not is_child
            )
            ttk.Frame.__init__(self, self.frame)
            ttk.Frame.pack(self, fill=tk.BOTH, expand=True, side=tk.TOP)
        else:
            ttk.Frame.__init__(self, parent)
        self.console = ScrolledText(
            self,
            textkw={"highlightthickness": 0, "state": tk.DISABLED},
        )
        self.console.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        self.entry = LabeledButtonEntry(
            self,
            labeltext=entrylabeltext,
            button_text=button_text,
            command=self._on_command,
            **kwargs
        )
        self.entry.pack(fill="x", expand=False, side=tk.TOP)

    def _on_command(self, event=None):
        """Calls the provided "command" function with the contents of the entry box. `Returns None`"""
        if self.command:
            self.command(self.entry.get().strip())
        self.entry.clear()

    def print(self, val, end: str = "\n"):
        """Prints a line to the console with a customizable line ending. `Returns None`"""
        self.console.configure(state=tk.NORMAL)
        self.console.insert(tk.END, val + end)
        self.console.configure(state=tk.DISABLED)


CONSOLE_WIDGETS = [ConsoleWidget]
