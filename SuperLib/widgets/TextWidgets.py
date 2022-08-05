#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from typing import Callable
from .Labeler import Labeler
from .Scroller import Scroller, _create_container
from .WidgetsCore import default_pack
from .WidgetsCore import SuperWidgetMixin


class ScrolledText(Scroller, tk.Text, SuperWidgetMixin):
    """Scrolled Textbox"""

    __desc__ = """Scrolled SuperWidget Text. Configure text by passing the `textkw` argument as a dict formatted like a standard kwarg dict."""

    @_create_container
    def __init__(self, parent, textkw: dict = {}, **kw):
        tk.Text.__init__(
            self,
            parent,
            wrap=tk.WORD,
            **textkw,
        )
        # Some systems don't bind this automatically
        self.bind("<Control-Key-a>", self.select_all, "+")
        Scroller.__init__(self, parent)
        SuperWidgetMixin.__init__(self, **kw)

    def select_all(self, event=None):
        """Selects all text. `Returns None`"""
        self.tag_add(tk.SEL, "1.0", tk.END)
        self.mark_set(tk.INSERT, "1.0")
        self.see(tk.INSERT)

    def set(self, val):
        """Sets the text. `Returns a String`"""
        state = self["state"]
        self.configure(state=tk.NORMAL)
        self.clear()
        self.insert("1.0", val)
        self.configure(state=state)

    def get(self, start="1.0", end=tk.END):
        """Returns the contents of the text box with optional start/end kwargs. `Returns a String`"""
        return tk.Text.get(self, start, end)

    def clear(self):
        """Empties the text box. `Returns None`"""
        self.delete("1.0", tk.END)

    def get_cursor(self):
        """Get the current location of the cursor. `Returns None`"""
        return tk.Text.index(self, tk.INSERT)

    def set_cursor(self, col, row):
        """Sets the cursor to a given col / row. `Returns None`"""
        text_widget_name.mark_set(tk.INSERT, "%d.%d" % (col, row))

    def enable(self):
        self.config(state="normal")

    def disable(self):
        self.config(state="disable")


class CopyBox(ttk.Frame):
    """Scrolled Text with "Copy tp Clipboard" Button"""

    __desc__ = "A widget with a scrolled textbox and button that copies the textbox contents to the user's clipboard. Useful for form output, etc."

    def __init__(self, parent: ttk.Frame, **kw):

        ttk.Frame.__init__(self, parent)
        self.button = ttk.Button(self, text="Copy to Clipboard", command=self._on_click)
        self.button.pack(side=tk.BOTTOM, fill="x", expand=False, pady=(0, 5))
        self.text = ScrolledText(self, textkw=kw)
        self.text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.get, self.set, self.clear = self.text.get, self.text.set, self.text.clear

    def _on_click(self):
        self.button.configure(text="Copied!")
        self.clipboard_clear()
        self.clipboard_append(self.get())
        self.after(1000, lambda: self.button.configure(text="Copy To Clipboard"))

    def enable(self):
        self.text.enable()

    def disable(self):
        self.text.disable()

TEXT_WIDGETS = [ScrolledText, CopyBox]
