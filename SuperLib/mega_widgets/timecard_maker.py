import tkinter as tk
from tkinter import ttk
from ..widgets.Tabs import Tab
from ..widgets.TextWidgets import CopyBox
from ..widgets.EntryWidgets import LabeledEntry
from ..widgets.ComboboxWidgets import LabeledCombobox

class TimecardTab(Tab):
    def __init__(self, notebook:ttk.Notebook):
        Tab.__init__(self, notebook, "Timecard Maker")
        TimecardMaker(self).pack(fill=tk.BOTH, expand="True")

DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
HOURS = [str(v) for v in range(0,25)]
MINUTES = [str(v) for v in range(0,60)]

class TimecardMaker(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        table_frame = ttk.Frame(self)
        table_frame.pack(side=tk.TOP, fill="x", padx=10)
        col = ttk.Frame(table_frame)
        col.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        ttk.Label(col, text="Day").pack(side=tk.TOP, fill="x")
        ttk.Label(col, text="Hours").pack(side=tk.TOP, fill="x")
        ttk.Label(col, text="Mins.").pack(side=tk.TOP, fill="x")
        self.columns = {}
        for d in DAYS:
            self.columns[d]=[]
            col = ttk.Frame(table_frame)
            col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            ttk.Label(col, text=d, anchor=tk.CENTER).pack(side=tk.TOP, fill="x")
            hourbox = LabeledCombobox(col, labeltext="", values=HOURS, is_child=True)
            hourbox.configure(width=0)
            hourbox.pack(side=tk.TOP, fill="x", expand=True)
            minutebox = LabeledCombobox(col, labeltext="", values=MINUTES, is_child=True)
            minutebox.configure(width=0)
            minutebox.pack(side=tk.TOP, fill="x", expand=True)
            self.columns[d] = (hourbox, minutebox)
        ttk.Button(self, command=self.generate, text="Generate Timecard").pack(side=tk.TOP, fill="x", expand=True, padx=10)
        ttk.Label(self, text='Use "Courier New" font in Outlook for correct spacing', justify=tk.CENTER, anchor=tk.CENTER).pack(side=tk.TOP, fill="x", expand=True)
        self.box = CopyBox(self)
        self.box.pack(side=tk.BOTTOM, fill="both", expand=True, padx=10)
        
    def generate(self):
        top_and_bottom ="+---------"
        top_row =       "|  Day    "
        middle_row =    "|  Hours  "
        bottom_row =    "|  Mins.  " 
        for d in DAYS:
            top_and_bottom += (len(d)+2)*"-"
            top_row += d+"  "
            hourstring = self.columns[d][0].get()
            hourstring += (5 - len(hourstring))*" "            
            middle_row += hourstring
            minutestring = self.columns[d][1].get()
            minutestring += (5 - len(minutestring))*" "            
            bottom_row += minutestring
        out = top_and_bottom+"+\n" + top_row + "|\n" + middle_row + "|\n" + bottom_row + "|\n" + top_and_bottom+"+"
        self.box.set(out)
