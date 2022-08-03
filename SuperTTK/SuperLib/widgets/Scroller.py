#!/usr/bin/python3
# -*- coding: utf-8 -*-

import platform
import tkinter as tk
from tkinter import ttk
from .Labeler import Labeler

# Widgets with scroll bars that appear when needed and supporting code
class Scroller(object):
    """Use to wrap an object with scrollbars"""

    def __init__(self, parent):
        try:
            vsb = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=self.xview)

        try:  # Fails if vsb instantiation failed
            self.configure(yscrollcommand=self._scroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._scroll(hsb))

        self.grid(column=0, row=0, sticky="nsew")
        try:
            vsb.grid(column=1, row=0, sticky="ns")
        except:
            pass
        hsb.grid(column=0, row=1, sticky="ew")

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)

        methods = (
            tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() | tk.Place.__dict__.keys()
        )

        for method in methods:
            if method[0] != "_" and method not in ("config", "configure"):
                setattr(self, method, getattr(parent, method))

    @staticmethod
    def _scroll(sbar):
        """Hide and show scrollbar as needed."""

        def hide(start, end):
            start, end = float(start), float(end)
            if start <= 0.0 and end >= 1.0:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(start, end)

        return hide

    def __str__(self):
        return str(self.parent)


def _create_container(func):
    """Creates a tk Frame with a given parent, and uses this new frame to place the scrollbars and the widget."""

    def wrapped(cls, parent, **kw):
        container = ttk.Frame(parent)
        container.bind("<Enter>", lambda e: _bound_to_mousewheel(e, container))
        container.bind("<Leave>", lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)

    return wrapped


def bind_mousewheel(widget):
    """Cross-platform mousewheel scrolling."""
    if platform.system() == "Windows" or platform.system() == "Darwin":
        widget.bind("<MouseWheel>", lambda e: _on_mousewheel(e, widget))
        widget.bind("<Shift-MouseWheel>", lambda e: _on_shiftmouse(e, widget))
    else:
        widget.bind("<Button-4>", lambda e: _on_mousewheel(e, widget))
        widget.bind("<Button-5>", lambda e: _on_mousewheel(e, widget))
        widget.bind("<Shift-Button-4>", lambda e: _on_shiftmouse(e, widget))
        widget.bind("<Shift-Button-5>", lambda e: _on_shiftmouse(e, widget))


def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == "Windows" or platform.system() == "Darwin":
        child.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, child))
        child.bind_all("<Shift-MouseWheel>", lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all("<Button-4>", lambda e: _on_mousewheel(e, child))
        child.bind_all("<Button-5>", lambda e: _on_mousewheel(e, child))
        child.bind_all("<Shift-Button-4>", lambda e: _on_shiftmouse(e, child))
        child.bind_all("<Shift-Button-5>", lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
    if platform.system() == "Windows" or platform.system() == "Darwin":
        widget.unbind_all("<MouseWheel>")
        widget.unbind_all("<Shift-MouseWheel>")
    else:
        widget.unbind_all("<Button-4>")
        widget.unbind_all("<Button-5>")
        widget.unbind_all("<Shift-Button-4>")
        widget.unbind_all("<Shift-Button-5>")


def _on_mousewheel(event, widget):
    if platform.system() == "Windows":
        widget.yview_scroll(-1 * int(event.delta / 120), "units")
    elif platform.system() == "Darwin":
        widget.yview_scroll(-1 * int(event.delta), "units")
    else:
        if event.num == 4:
            widget.yview_scroll(-1, "units")
        elif event.num == 5:
            widget.yview_scroll(1, "units")


def _on_shiftmouse(event, widget):
    if platform.system() == "Windows":
        widget.xview_scroll(-1 * int(event.delta / 120), "units")
    elif platform.system() == "Darwin":
        widget.xview_scroll(-1 * int(event.delta), "units")
    else:
        if event.num == 4:
            widget.xview_scroll(-1, "units")
        elif event.num == 5:
            widget.xview_scroll(1, "units")
