from tkinter import Canvas
from .WidgetsCore import create_round_rectangle

class ResizableCanvas(Canvas):
    """Resizeable Canvas"""

    __desc__ = "Canvas resizes to fit frame on configure event."
    def __init__(self, parent, **kw):
        Canvas.__init__(self, parent)
        self.configure(borderwidth=0)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.bind("<Configure>", self._on_resize, add="+")

    def create_round_rectangle(self, x1:float, y1:float, x2:float, y2:float, r:float=20, fill:str="", outline:str="#000000", **kwargs):
        """Draws a rounded rectangle of a given radius on a tk.canvas."""
        return create_round_rectangle(self, x1, y1, x2, y2, r=r, fill=fill, outline=outline, **kwargs)

    def _resize(self, newwidth, newheight):
        wscale = newwidth / self.width
        hscale = newheight / self.height
        self.config(width=newwidth, height=newheight)
        self.scale("all", 0, 0, wscale, hscale)
        self.width = newwidth
        self.height = newheight

    def _on_resize(self, event):
        self._resize(event.width, event.height)

    def refresh(self):
        """Refresh Canvas"""
        self._resize(
            self.winfo_reqwidth(), self.winfo_reqheight()
        )
