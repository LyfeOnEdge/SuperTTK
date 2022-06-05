import tkinter as tk
from tkinter import ttk

#Apply a consistent separator
def default_separator(f:ttk.Frame,padx=35,pady=(10,5)): ttk.Separator(f,orient='horizontal').pack(fill='x',padx=padx,pady=pady)
#apply a consistent packing method
def default_pack(widget, bottom=False): widget.pack(fill='x', expand=False, side=tk.TOP, padx=5, pady=(0,5*bottom))
#Apply a consistent vertical separator
def default_vertical_separator(f:ttk.Frame,pady=15,padx=10): ttk.Separator(f,orient='vertical').pack(fill='y',padx=padx,pady=pady,expand=False,side=tk.LEFT)
#apply a consistent packing method to vertical widgets
def default_vertical_pack(widget,expand=False,padx=0): widget.pack(fill='both',expand=expand,side=tk.LEFT,padx=padx)
def copy_to_user_clipboard(widget, value):
	widget.clipboard_clear()
	widget.clipboard_append(value)
def recursive_widget_search(node_widget, widget_type_to_find, found_list=[]):
	'''
	Adds widgets of a given type to a list as it travels up, away from the root of a widget tree.
	This method can be slow on large widget trees but is useful for retheming tk widgets with
	ttk formatting on theme changes
	'''
	for w in node_widget.winfo_children():
		if isinstance(w, widget_type_to_find):
			found_list.append(w)
		else:
			recursive_widget_search(w, widget_type_to_find, found_list)
	return found_list #The only time this return is ever used is at the end of the first call