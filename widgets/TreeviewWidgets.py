from tkinter import ttk
from .Scroller import Scroller, _create_container
from .WidgetsCore import SuperWidgetMixin


class ScrolledTree(Scroller, ttk.Treeview, SuperWidgetMixin):
    @_create_container
    def __init__(self, parent, treekw: dict, **kw):
        Treeview.__init__(self, parent, **treekw)
        Scroller.__init__(self, parent)
        SuperWidgetMixin.__init__(self, **kw)
