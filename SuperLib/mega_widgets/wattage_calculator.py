import tkinter as tk
from tkinter import ttk
from ..widgets.Tabs import Tab
from ..widgets.EntryWidgets import LabeledEntry
from ..widgets.ComboboxWidgets import LabeledCombobox
from ..widgets.TextWidgets import CopyBox
from ..widgets.WidgetsCore import default_pack

def round_to(x, base=5):
    return 5 * round(x/5)

class WattageTab(Tab):
    def __init__(self, notebook:ttk.Notebook):
        Tab.__init__(self, notebook, "Wattage Calculator")
        WattageCalculator(self).pack(fill=tk.BOTH, expand="True")

class WattageCalculator(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        def calc(_):
            try:
                amps = float(amperage_entry.get())
                volts = float(voltage_entry.get())
                watts = amps * volts
                output.set(str(round_to(watts)))
            except:
                output.set("Error")
            
        amperage_entry = LabeledEntry(self, labeltext="Amperage (A): ", on_keystroke=True, command=calc)
        default_pack(amperage_entry, padx=10)
        voltage_entry = LabeledEntry(self, labeltext="Voltage (V): ", on_keystroke=True, command=calc)
        default_pack(voltage_entry, padx=10)
        ttk.Label(self, text="Wattage (Rounded to multiple of 5): ", justify=tk.CENTER, anchor=tk.CENTER).pack(side=tk.TOP, fill="x", pady=(10,0))
        output = CopyBox(self, height=1)
        output.disable()
        output.pack(side=tk.TOP, pady=(0, 10), expand=False, fill="x", padx=10)
