import tkinter as tk
from tkinter import ttk
from .Scroller import Scroller, _create_container
from .WidgetsCore import SuperWidgetMixin

class ScrolledTree(Scroller, ttk.Treeview, SuperWidgetMixin):
    """A Scrolled Listbox-style Treeview with the SuperWidget Mixin"""
    @_create_container
    def __init__(self, parent, tree_config: dict={}, min_column_width = 100, set_width = None, **kw):
        ttk.Treeview.__init__(self, parent, **tree_config)
        Scroller.__init__(self, parent)
        SuperWidgetMixin.__init__(self, **kw)
        self.column("#0", width = 0, stretch = "no")
        # self['show'] = 'headings'
        for c in tree_config['columns']:
            self.heading(c, text=c,anchor=tk.W)
            self.column(c,minwidth=min_column_width)
            if not set_width is None:
                self.column(c, width=set_width)

class TreeTable(ScrolledTree): #Each kw in the dict is a table header
    def __init__(self,*args,table_contents:dict={}, **kw):
        ScrolledTree.__init__(self,*args,tree_config={'columns':list(table_contents.keys())},**kw)
        self.table_contents = table_contents
        for k in table_contents:
            self.table_contents[k] = list(table_contents[k])
        if self.table_contents:
            length = len(list(self.table_contents[k]))
            if length:
                for i in range(length):
                    self.insert('', tk.END, values=[self.table_contents[k][i] for k in self.table_contents])

        # self.tag_configure('oddrow', background='orange')
        # self.tag_configure('evenrow', background='purple')
