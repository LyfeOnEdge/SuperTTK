#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from .Labeler import Labeler
from .MultiWidget import MultiWidgetMixin
from typing import Callable

class LabeledEntry(Labeler, ttk.Entry):
	def __init__(
				self,parent:ttk.Frame,labeltext:str,command:Callable=None,\
				default:str='',on_keystroke:bool=False,bind_enter:bool=True,\
				bind_escape_clear:bool=True,is_child:bool=False
			):
		self.var = tk.StringVar()
		self.var.set(default)
		Labeler.__init__(self, parent,labeltext,header=not is_child)
		ttk.Entry.__init__(self,self.frame,textvariable=self.var)
		ttk.Entry.pack(self,fill='both',expand=True,side=tk.TOP)
		self.default=default
		self.is_child=is_child
		self._command=command
		if on_keystroke:self.bind("<KeyRelease>",self._on_execute_command)
		if bind_enter:self.bind("<Return>",self._on_execute_command)
		if bind_escape_clear:self.bind("<Escape>",self.clear())
	def enable(self): self['state']=tk.NORMAL
	def disable(self): self['state']=tk.DISABLED
	def get(self): return self.var.get()
	def set(self, val):self.var.set(val)
	def clear(self):self.var.set(self.default)
	def _on_execute_command(self, event=None):
		if self._command:self._command(self.get())

class LabeledMultiEntry(Labeler, ttk.Frame, MultiWidgetMixin):
	def __init__(self,parent:ttk.Frame,labeltext:str,config:dict,is_child:bool=False,labelside=tk.TOP):
		Labeler.__init__(self,parent,labeltext,labelside=labelside,header=not is_child)
		ttk.Frame.__init__(self, self.frame)
		ttk.Frame.pack(self,fill='both',expand=True,side=tk.TOP)
		MultiWidgetMixin.__init__(self,LabeledEntry,config)
		self.is_child = is_child

class LabeledButtonEntry(LabeledEntry):
	def __init__(self,*args,**kwargs):
		if not kwargs.get('buttontext'): raise ValueError('LabeledButtonEntry missing required argument "buttontext"')
		buttontext = kwargs.pop('buttontext')
		LabeledEntry.__init__(self,*args,**kwargs)
		self.button = ttk.Button(self, command=self._on_execute_command, text=buttontext)
		self.button.pack(expand=False, side=tk.RIGHT)