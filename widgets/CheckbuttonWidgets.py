#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from .Labeler import Labeler
from .MultiWidget import MultiWidgetMixin

class LabeledCheckbutton(Labeler, ttk.Checkbutton):
	def __init__(
				self,parent:ttk.Frame,labeltext:str,buttontext:str=None,\
				replace_output:list=None,default:bool=False,\
				is_child:bool=False
			):
		self.var = tk.IntVar()
		self.default = default
		self.var.set(default)
		self.replace_output = replace_output
		self.is_child = is_child
		Labeler.__init__(self, parent, labeltext, header=not is_child)
		ttk.Checkbutton.__init__(self, self.frame, variable=self.var, text=buttontext)
		ttk.Checkbutton.pack(self,fill='x',expand=False,side=tk.TOP)
	def enable(self): self['state']=tk.NORMAL
	def disable(self): self['state']=tk.DISABLED
	def get(self):
		v = self.var.get()
		return self.replace_output[v] if self.replace_output else v
	def set(self, val:bool): self.var.set(val)
	def clear(self): self.var.set(self.default)

class LabeledMultiCheckbutton(Labeler, ttk.Frame, MultiWidgetMixin):
	def __init__(self,parent:ttk.Frame,labeltext:str,config:dict,is_child:bool=False,labelside=tk.TOP):
		Labeler.__init__(self,parent,labeltext,labelside=labelside,header=not is_child)
		ttk.Frame.__init__(self, self.frame)
		ttk.Frame.pack(self,fill='both',expand=True,side=tk.TOP)
		MultiWidgetMixin.__init__(self,LabeledCheckbutton,config)
		self.is_child = is_child