#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk


class Labeler:
    """Makes a frame and a label for a widget, used as a mixin"""

    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str,
        labelside: str = tk.LEFT,
        header: bool = False,
    ):
        self.frame = ttk.Frame(parent)
        self.label = ttk.Label(
            self.frame, text=labeltext, style=["TLabel", "Bold.TLabel"][header]
        )
        self.label.pack(fill="x", expand=False, side=labelside)

    def pack(self, *args, **kw):
        self.frame.pack(*args, **kw)

    def set_label_text(self, val: str):
        self.label.configure(text=val)
