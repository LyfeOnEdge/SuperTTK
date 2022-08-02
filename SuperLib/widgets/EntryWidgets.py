#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from typing import Callable
from .Labeler import Labeler
from .MultiWidget import MultiWidgetMixin
from .Scroller import Scroller, _create_container
from .WidgetsCore import SuperWidgetMixin, focus_next, get_asset
from .ToolTip import ToolTip
import sys


class ScrolledEntry(Scroller, ttk.Entry, SuperWidgetMixin):
    """Scrolled ttk.Entry with SuperWidgetMixin"""

    __desc__ = """This class is here for completeness but most of the time you will \
want to use the ScrolledText widget. Used when you need a scrollable text entry box."""

    @_create_container
    def __init__(self, parent: ttk.Frame, widgetargs:dict={}, **kw):
        ttk.Entry.__init__(
            self,
            parent,
            **kw,
        )
        Scroller.__init__(self, parent)
        SuperWidgetMixin.__init__(self, **widgetargs)


class LabeledEntry(Labeler, ttk.Entry, SuperWidgetMixin):
    """Labeled ttk.Entry with SuperWidgetMixin"""

    __desc__ = """Used when you need a Labeled Entry"""

    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str,
        command: Callable = None,
        default: str = "",
        on_keystroke: bool = False,
        bind_enter: bool = True,
        bind_escape_clear: bool = True,
        is_child: bool = False,
        min_width: int = 0,
        widgetargs={},
        **kw
    ):
        self.var = tk.StringVar()
        self.var.set(default)
        Labeler.__init__(self, parent, labeltext, header=not is_child)
        ttk.Entry.__init__(
            self, self.frame, textvariable=self.var, width=min_width, **kw
        )
        ttk.Entry.pack(self, fill=tk.BOTH, expand=True, side=tk.TOP)
        SuperWidgetMixin.__init__(self, **widgetargs)
        self.default = default
        self.is_child = is_child
        self._command = command
        if on_keystroke:
            self.bind("<KeyRelease>", self._on_execute_command)
        if bind_enter:
            self.bind("<Return>", self._on_execute_command)
        if bind_escape_clear:
            self.bind("<Escape>", self.clear())

    def enable(self):
        """Enable Entry. `Returns None`"""
        self["state"] = tk.NORMAL

    def disable(self):
        """Disable Entry. `Returns None`"""
        self["state"] = tk.DISABLED

    def get(self):
        """Get Entry value. `Returns a String`"""
        return self.var.get()

    def set(self, val):
        """Set Entry value. `Returns None`"""
        self.var.set(val)

    def clear(self):
        """Set Entry value to default, empty unless default set. `Returns None`"""
        self.var.set(self.default)

    def _on_execute_command(self, event=None):
        """Calls the provided "command" function with the contents of the Entry. `Returns None`"""
        if self._command:
            self._command(self.get())


class LabeledMultiEntry(Labeler, ttk.Frame, MultiWidgetMixin):
    """Labeled MultiWidget LabeledEntry"""

    __desc__ = """Used when you need multiple, vertically stacked Labeled Entries"""

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
        MultiWidgetMixin.__init__(self, LabeledEntry, config)
        self.is_child = is_child


class LabeledButtonEntry(LabeledEntry):
    """LabeledEntry with a ttk.Button on the right"""

    def __init__(self, *args, button_text="", **kwargs):
        LabeledEntry.__init__(self, *args, **kwargs)
        self.button = ttk.Button(
            self, command=self._on_execute_command, text=button_text
        )
        self.button.pack(expand=False, side=tk.RIGHT)


class PasswordEntry(ttk.Frame):
    """Username / Password Entry"""

    __desc__ = "A username/password entry widget with optional password peeking. Set password_char \
to `''` to show password by default. The provided command will always be called with the \
tuple `(username_entry.get(), password_entry.get())` as the only argument even if one of the \
entries is disabled."

    def __init__(
        self,
        *args,
        instruction_text:str="",
        username_text:str="Username: ",
        username_enabled:bool=True,
        password_text:str="Password: ",
        password_enabled:bool=True,
        button_text:str="Submit",
        command=print,
        password_char:str="*",
        peek_enabled:bool=True,
        invert_peek_colors:bool=False,
        **kwargs
    ):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.command = command
        if instruction_text:
            t = ttk.Label(self, text=instruction_text).pack(side=tk.TOP)
        self.username_entry = LabeledEntry(self, labeltext=username_text)
        self.username_entry.bind("<Return>", focus_next)
        if username_enabled:
            self.username_entry.pack(side=tk.TOP, anchor="n", fill="x", expand=True)
        f = ttk.Frame(self)
        f.pack(fill="x", expand=True)
        self.password_entry = LabeledEntry(f, labeltext=password_text)
        self.password_entry.configure(show=password_char)
        self.password_entry.bind("<Return>", self.on_submit)
        if password_enabled:
            self.password_entry.pack(side=tk.LEFT, anchor="n", fill="x", expand=True)
            if peek_enabled:
                self.peek = [
                    tk.PhotoImage(file=get_asset("eye_16_black.png")),
                    tk.PhotoImage(file=get_asset("eye_16_white.png")),
                ]
                if invert_peek_colors:
                    self.peek = list(reversed(self.peek))
                self.peek_button = ttk.Button(
                    f,
                    width=0,
                    image=self.peek[0],
                    style="NoPad.TButton",
                )
                self.peek_button.pack(
                    side=tk.RIGHT, expand=False, ipadx=0, ipady=0, padx=0, pady=0
                )
                self.peek_button.bind("<Button-1>", self.on_peek_press)
                self.peek_button.bind("<ButtonRelease-1>", self.on_peek_release)
                ToolTip(self.peek_button, "Peek at password", align=tk.RIGHT)

        ttk.Button(self, text=button_text, command=self.on_submit).pack(
            side=tk.TOP, fill="x", expand=False
        )

    def on_peek_press(self, event=None):
        """Show the contents of the password entry while it is being pressed"""
        self.password_entry.configure(show="")
        self.peek_button.configure(image=self.peek[1])

    def on_peek_release(self, event=None):
        """Rehide the contents of the password entry"""
        self.password_entry.configure(show="*")
        self.peek_button.configure(image=self.peek[0])

    def on_submit(self, event=None):
        """Calls the provided "command" function with the contents of the entry box. `Returns None`"""
        if self.command:
            self.command((self.username_entry.get(), self.password_entry.get()))


ENTRY_WIDGETS = [
    ScrolledEntry,
    LabeledEntry,
    LabeledMultiEntry,
    LabeledButtonEntry,
    PasswordEntry,
]
