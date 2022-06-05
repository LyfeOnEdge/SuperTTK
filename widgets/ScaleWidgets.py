#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from .Labeler import Labeler
from .MultiWidget import MultiWidgetMixin
from typing import Callable

class LabeledScale(Labeler, ttk.Scale):
	def __init__(
				self,parent:ttk.Frame,labeltext:str,command:Callable=None,\
				default:float=0,orient:bool=tk.HORIZONTAL,is_child:bool=False,\
				from_=0, to=100, **kwargs
			):
		self.var = tk.DoubleVar()
		self.var.set(default)
		self.default = default
		self.is_child = is_child
		self._command = command
		kwargs['from_']=from_
		kwargs['to']=to
		if orient==tk.HORIZONTAL:
			Labeler.__init__(self,parent,labeltext,header=not is_child)
			ttk.Scale.__init__(self,self.frame,variable=self.var,command=self._on_update,**kwargs)
			ttk.Scale.pack(self,fill='x',expand=True,side=tk.TOP)
		elif orient==tk.VERTICAL:
			Labeler.__init__(self,parent,labeltext,labelside=tk.TOP,header=not is_child)
			ttk.Scale.__init__(self,self.frame,variable=self.var,command=self._on_update,orient=tk.VERTICAL,**kwargs)
			ttk.Scale.pack(self,fill='y',expand=True,side=tk.TOP)
		else:
			raise ValueError(f"Unknown orientation - {orient}")
	def enable(self): self['state']=tk.NORMAL
	def disable(self): self['state']=tk.DISABLED
	def get(self): return self.var.get()
	def set(self, val):self.var.set(val)
	def clear(self):self.var.set(self.default)
	def _on_update(self, val):
		if self._command:self._command(val)

class LabeledMultiScale(Labeler, ttk.Frame, MultiWidgetMixin):
	def __init__(self,parent:ttk.Frame,labeltext:str,config:dict,is_child:bool=False,labelside=tk.TOP,orient=tk.HORIZONTAL,command=None):
		self.orient = orient
		self.is_child = is_child
		self._command = command
		Labeler.__init__(self,parent,labeltext,labelside=labelside,header=not is_child)
		ttk.Frame.__init__(self, self.frame)
		ttk.Frame.pack(self,fill='both',expand=True,side=tk.TOP)
		MultiWidgetMixin.__init__(self,LabeledScale,config)

	def _on_command(self, key):
		def do_command(val):
			if self._command:
				return self._command({key:val})
		return do_command
		
	#Override MultiWidgetMixin for vertical orientation
	def add(self,parent,key,args,kwargs,widget_type=None):
		widget_type = widget_type or self.widget_type
		kwargs['orient']=self.orient

		w = widget_type(parent,key,*args,command=self._on_command(key),**kwargs)
		if self.orient == tk.HORIZONTAL:
			w.pack(fill='x',expand=False,side=tk.TOP,padx=(20,0))
		elif self.orient==tk.VERTICAL:
			w.pack(fill='y',expand=True,side=tk.LEFT)
		else:
			raise ValueError(f'Bad orientation - {self.orient}')
		self.widgets[key]=w