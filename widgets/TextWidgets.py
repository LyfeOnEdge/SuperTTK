#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from typing import Callable
from .Labeler import Labeler
from .Scroller import Scroller, _create_container
from .WidgetsCore import default_pack

class ScrolledText(Scroller, tk.Text):
	'''Scrolled Textbox'''
	@_create_container
	def __init__(self, master, **kw):
		tk.Text.__init__(self, master, wrap=tk.WORD, **kw)
		Scroller.__init__(self, master)

	def set(self, val):
		state = self["state"]
		self.configure(state=tk.NORMAL)
		self.clear()
		self.insert('1.0', val)
		self.configure(state=state)
	def get(self):return tk.Text.get(self, "1.0", tk.END)
	def clear(self):self.delete('1.0', tk.END)

class CopyBox(ScrolledText):
	def __init__(self, master, **kw):
		container = ttk.Frame(master)
		container.pack(fill='both',expand=True,side=tk.TOP)
		ScrolledText.__init__(self, container, **kw)
		self.copy_button = ttk.Button(container, command=self.on_click, text="Copy To Clipboard")
		self.copy_button.pack(fill='x', expand=False, side=tk.BOTTOM, pady=(0,5), padx=5)

	def on_click(self):
		self.copy_button.configure(text='Copied!')
		self.clipboard_clear()
		self.clipboard_append(self.get())
		self.after(1000, lambda:self.copy_button.configure(text='Copy To Clipboard'))