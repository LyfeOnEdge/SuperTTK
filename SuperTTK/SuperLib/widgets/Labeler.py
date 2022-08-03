#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk


class Labeler:
    """Mixin to add a ttk label to a widget."""

    __desc__ = """Makes a frame and a label for a widget, used as a mixin. With some labeled/multiwidgets repositioning the label may not always work as expected. The label is on the left side of the widget by default. The Labeler object creates a self.frame (ttk.Frame) that other mix-ins/children widges should use."""

    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str,
        labelside: str = tk.LEFT,
        header: bool = False,
    ):
        self.frame = ttk.Frame(parent)
        self.labelvar = tk.StringVar()
        self.labelvar.set(labeltext)
        self.label = ttk.Label(
            self.frame,
            textvariable=self.labelvar,
            style=["TLabel", "Bold.TLabel"][header],
        )
        self.label.pack(fill="x", expand=False, side=labelside)

    def pack(self, *args, **kw):
        """Forward pack args to container frame."""
        self.frame.pack(*args, **kw)

    def set_label_text(self, val: str):
        """Update a Labeled widget's Label text."""
        self.label.configure(text=val)
