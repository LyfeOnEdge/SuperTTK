import subprocess
import webbrowser
import tkinter as tk
from tkinter import ttk
from typing import Callable
from .WidgetsCore import open_link, run_cl
from .ConsoleWidgets import ConsoleWidget
from .ListBoxWidgets import Table
from .TreeviewWidgets import TreeTable

class Tab(ttk.Frame):
    """The core Tab class."""

    __desc__ = """The notebook object can be any ttk.Notebook, automatically adds itself to its parent notebook with title being the tab label. This class may be instantiated directly and added to or subclassed based on need."""

    def __init__(self, notebook: ttk.Notebook, title: str):
        ttk.Frame.__init__(self, notebook)
        notebook.add(self, text=title)

class LauncherTab(Tab):
    """Basic Tab for launching tasks from a list."""

    __desc__ = """Performs an action on a list of options. The options argument is formatted as such: `options = {"Button Text 1": val1,"Button Text 2": val2}` Button presses will call `action(val)`"""

    def __init__(
        self, notebook: ttk.Notebook, title: str, options: dict, action: Callable
    ):
        Tab.__init__(self, notebook, title)
        for title in options:
            button = ttk.Button(
                self, text=title, command=lambda title=title: action(options[title])
            )
            button.pack(fill="x", expand=False, side=tk.TOP)


class CommandLauncherTab(LauncherTab):
    """LauncherTab that runs a list of commands"""

    __desc__ = """Takes a dict of button texts as keys and command prompt commands to execute as values"""

    def __init__(self, notebook: ttk.Notebook, title: str, options: dict):
        LauncherTab.__init__(self, notebook, title, options, run_cl)


class BrowserLauncherTab(LauncherTab):
    """LauncherTab that opens a list of URLS/Files"""

    __desc__ = """Takes a dict of button texts as keys and urls to open as values"""

    def __init__(self, notebook: ttk.Notebook, title: str, options: dict):
        LauncherTab.__init__(self, notebook, title, options, open_link)


class ConsoleTab(Tab):
    """Basic console tab using a ConsoleWidget"""

    def __init__(self, notebook: ttk.Notebook, **kwargs):
        Tab.__init__(self, notebook, "Console")
        self.console = ConsoleWidget(self, **kwargs)
        self.console.pack(fill=tk.BOTH, expand=True)


class TableTab(Tab):
    """Basic Table Tab"""

    __desc__="""table_contents is a dictionary whose keys map to lists with the column contents"""

    def __init__(self, notebook: ttk.Notebook, title: str, table_contents: dict, **kw):
        Tab.__init__(self, notebook, title)
        self.table = Table(self, **kw)
        self.table.pack(expand=True, fill=tk.BOTH)
        self.table.build(table_contents)
        self.info_var = tk.StringVar()


class TreeTableTab(Tab):
    """Improved Table Tab"""

    __desc__ = """table_contents is a dictionary whose keys map to list with the column contents"""

    def __init__(
        self, notebook: ttk.Notebook, title: str, table_contents: dict = {}, **kw
    ):
        Tab.__init__(self, notebook, title)
        self.table = TreeTable(self, table_contents=table_contents, **kw)
        self.table.pack(expand=True, fill=tk.BOTH)


TABS = [
    Tab,
    LauncherTab,
    BrowserLauncherTab,
    CommandLauncherTab,
    ConsoleTab,
    TableTab,
    TreeTableTab,
]
