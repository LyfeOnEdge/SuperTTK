# Based on https://github.com/roseman/idle/blob/master/ToolTip.py
# Modified to be consistent with this project
import tkinter as tk
from tkinter import ttk
from .TextWidgets import ScrolledText

# Tooltip
class ToolTipBase:
    def __init__(self, tipwidget, align=tk.LEFT):
        self.tipwidget, self.align = tipwidget, align
        self.id, self.tipwindow = None, None
        self.x = self.y = 0
        self._id1 = self.tipwidget.bind("<Enter>", self._enter)
        self._id2 = self.tipwidget.bind("<Leave>", self._leave)
        self._id3 = self.tipwidget.bind("<ButtonPress>", self._leave)

    def _enter(self, event=None):
        self._schedule()

    def _leave(self, event=None):
        self._unschedule()
        self._hidetip()

    def _schedule(self):
        self._unschedule()
        self.id = self.tipwidget.after(10, self._showtip)

    def _unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.tipwidget.after_cancel(id)

    def _showtip(self):
        if self.tipwindow:
            return
        self.tipwindow = tk.Toplevel(self.tipwidget)
        self.tipwindow.wm_overrideredirect(1)
        self._showcontents()
        self.tipwindow.update_idletasks()

        x = self.tipwidget.winfo_rootx()
        y = self.tipwidget.winfo_rooty() + self.tipwidget.winfo_height() + 1

        if self.align == tk.LEFT:
            pass
        elif self.align == tk.RIGHT:
            x += self.tipwidget.winfo_width() - self.tipwindow.winfo_width()
        else:
            raise ValueError(f"Unsupported ToolTip alignment {self.align}")
        self.tipwindow.wm_geometry("+%d+%d" % (x, y))

    def _showcontents(self, text=""):
        sc = ttk.Label(self.tipwindow, text=text, borderwidth=2, relief=tk.SOLID)
        sc.pack()

    def _hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


class ToolTip(ToolTipBase):
    """Easy ToolTip"""

    __desc__ = """Easily show theme-friendly tooltip. Currently only left and right align are supported."""
    
    def __init__(self, tipwidget, text:str, align=tk.LEFT):
        ToolTipBase.__init__(self, tipwidget, align)
        self.text = text

    def _showcontents(self):
        ToolTipBase._showcontents(self, self.text)
