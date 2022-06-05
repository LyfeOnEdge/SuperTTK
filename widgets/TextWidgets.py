#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from typing import Callable
from .Labeler import Labeler
from .Scroller import Scroller, _create_container

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