#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from .Labeler import Labeler
from .MultiWidget import MultiWidgetMixin

class LabeledRadiobutton(Labeler, ttk.Frame):
	def __init__(
				self,parent:ttk.Frame,labeltext:str,\
				options:list=[],default:int=0,is_child:bool=False, \
			):
		self.var = tk.StringVar()
		self.default = options[default]
		self.var.set(self.default)
		self.is_child = is_child
		Labeler.__init__(self, parent, labeltext, header=not is_child,labelside=tk.TOP)
		ttk.Frame.__init__(self, self.frame)
		ttk.Frame.pack(self,fill='both',expand=True,side=tk.LEFT)
		for o in options:
			b = ttk.Radiobutton(self, text=o,value=o,variable=self.var)
			b.pack(fill='x',expand=False,side=tk.TOP,padx=(20,0))
	def enable(self): self['state']=tk.NORMAL
	def disable(self): self['state']=tk.DISABLED
	def get(self):return self.var.get()
	def set(self, val:bool): self.var.set(val)
	def clear(self): self.var.set(self.default)

class LabeledMultiRadiobutton(Labeler, ttk.Frame, MultiWidgetMixin):
	def __init__(self,parent:ttk.Frame,labeltext:str,config:dict,is_child:bool=False,labelside=tk.TOP):
		Labeler.__init__(self,parent,labeltext,labelside=labelside,header=not is_child)
		ttk.Frame.__init__(self, self.frame)
		ttk.Frame.pack(self,fill='both',expand=True,side=tk.TOP)
		MultiWidgetMixin.__init__(self,LabeledRadiobutton,config)
		self.is_child = is_child