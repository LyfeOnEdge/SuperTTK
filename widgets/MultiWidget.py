import tkinter as tk
from tkinter import ttk


class MultiWidgetMixin:
    def __init__(self, widget_type, config: dict):
        self.widget_type = widget_type
        self.widgets = {}
        for k in config:
            args, kwargs = config[k]
            kwargs["is_child"] = True
            self.add(self, k, args, kwargs)

    # Widget type for adding different kinds of widgets to a group after normal instantiation
    def add(self, parent, key, args, kwargs, widget_type=None):
        widget_type = widget_type or self.widget_type
        w = widget_type(parent, key, *args, **kwargs)
        w.pack(fill="x", expand=False, side=tk.TOP, padx=(20, 0))
        self.widgets[key] = w

    def get(self, config: list = None):
        """Pass a list of wiget keys to get a dict of outputs"""
        out = {}
        widgets = config if config else self.widgets
        for w in widgets:
            out[w] = self.widgets[w].get()
        return out

    def set(self, config: dict):
        """Pass a map of widget keys and their values"""
        for w in config:
            self.widgets[w].set(config[w])

    def enable(self, config: list = None):
        """Pass a list of subwidgets to enable or all are enabled"""
        widgets = config if config else self.widgets
        for w in widgets:
            self.widgets[w].enable()

    def disable(self, config: list = None):
        """Pass a list of subwidgets to disable or all are disabled"""
        widgets = config if config else self.widgets
        for w in widgets:
            self.widgets[w].disable()

    def clear(self, config: list = None):
        """Pass a list of subwidgets to clear or all are set to default"""
        widgets = config if config else self.widgets
        for w in widgets:
            self.widgets[w].clear()
