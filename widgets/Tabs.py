import subprocess
import webbrowser
import tkinter as tk
from tkinter import ttk
from typing import Callable
from .WidgetsCore import open_link, run_cl
from .ConsoleWidgets import ConsoleWidget
from .ListBoxWidgets import Table
from .TreeviewWidgets import TreeTable

# Tabs add themselves self to their parent notebook
class Tab(ttk.Frame):
    def __init__(self, notebook: ttk.Notebook, title: str):
        ttk.Frame.__init__(self, notebook)
        notebook.add(self, text=title)


class LauncherTab(Tab):
    def __init__(
        self, notebook: ttk.Notebook, title: str, options: dict, action: Callable
    ):
        Tab.__init__(self, notebook, title)
        # inner_frame = ttk.Frame(self)
        # inner_frame.pack(fill=tk.BOTH, expand=True)
        for title in options:
            button = ttk.Button(
                self, text=title, command=lambda title=title: action(options[title])
            )
            button.pack(fill="x", expand=False, side=tk.TOP)


class CommandLauncherTab(LauncherTab):
    def __init__(self, notebook: ttk.Notebook, title: str, options: dict):
        LauncherTab.__init__(self, notebook, title, options, run_cl)


class BrowserLauncherTab(LauncherTab):
    def __init__(self, notebook: ttk.Notebook, title: str, options: dict):
        LauncherTab.__init__(self, notebook, title, options, open_link)


class ConsoleTab(Tab):
    def __init__(self, notebook: ttk.Notebook, **kwargs):
        Tab.__init__(self, notebook, "Console")
        self.console = ConsoleWidget(self, **kwargs)
        self.console.pack(fill="both", expand=True)


class ScrolledButtonTab(Tab):
    def __init__(self, notebook: ttk.Notebook, title: str, options: dict):
        Tab.__init__(self, notebook, title)
        self.buttons = ScrolledButtons(self)
        self.buttons.pack(fill="both", expand=True)

class TableTab(Tab):
    def __init__(
        self,
        notebook: ttk.Notebook,
        title: str,
        table_contents: dict,
        **kw
    ):
        Tab.__init__(self, notebook, title)
        self.table = Table(self, **kw)
        self.table.pack(expand=True, fill=tk.BOTH)
        self.table.build(table_contents)
        self.info_var = tk.StringVar()

class TreeTableTab(Tab):
    def __init__(
        self,
        notebook: ttk.Notebook,
        title: str,
        table_contents:dict={},
        # options: dict,
        **kw
    ):
        Tab.__init__(self, notebook, title)
        self.table = TreeTable(self, table_contents=table_contents,**kw)
        self.table.pack(expand=True, fill=tk.BOTH)
        # self.table.build(options)
        # self.info_var = tk.StringVar()