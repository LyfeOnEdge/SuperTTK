#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from .Labeler import Labeler
from .MultiWidget import MultiWidgetMixin

class LabeledProgressbar(Labeler, ttk.Progressbar):
	def __init__(self,parent:ttk.Frame,labeltext:str,orient=tk.HORIZONTAL,labelside=tk.LEFT,is_child=False,default:float=0,**kw):
		self.is_child = is_child
		if orient==tk.HORIZONTAL:
			Labeler.__init__(self,parent,labeltext,labelside=labelside,header=not is_child)
			ttk.Progressbar.__init__(self,self.frame,**kw)
			ttk.Progressbar.pack(self,fill='x',expand=True,side=tk.RIGHT)
		elif orient==tk.VERTICAL:
			Labeler.__init__(self,parent,labeltext,labelside=tk.TOP,header=not is_child)
			ttk.Progressbar.__init__(self,self.frame,orient=tk.VERTICAL,**kw)
			ttk.Progressbar.pack(self,fill='y',expand=True,side=tk.TOP)
		else:
			raise ValueError(f"Bad orientation - {orient}")
	def enable(self): self['state']=tk.NORMAL
	def disable(self): self['state']=tk.DISABLED
	def set(self, val):self['value']=val
	def get(self):return self['value']
	def link(self, widget):self.configure(variable=widget.var) #Easily link to other widgets


class LabeledMultiProgressbar(Labeler, ttk.Frame, MultiWidgetMixin):
	def __init__(self,parent:ttk.Frame,labeltext:str,config:dict,is_child:bool=False,labelside=tk.TOP,orient=tk.HORIZONTAL):
		self.orient = orient
		self.is_child = is_child
		Labeler.__init__(self,parent,labeltext,labelside=labelside,header=not is_child)
		ttk.Frame.__init__(self, self.frame)
		ttk.Frame.pack(self,fill='both',expand=True,side=tk.TOP)
		MultiWidgetMixin.__init__(self,LabeledProgressbar,config)
		
	#Override MultiWidgetMixin for vertical orientation
	def add(self,parent,key,args,kwargs,widget_type=None):
		widget_type = widget_type or self.widget_type
		kwargs['orient']=self.orient
		w = widget_type(parent,key,*args,**kwargs)
		if self.orient == tk.HORIZONTAL:
			w.pack(fill='x',expand=False,side=tk.TOP,padx=(20,0))
		elif self.orient==tk.VERTICAL:
			w.pack(fill='y',expand=True,side=tk.LEFT)
		else:
			raise ValueError(f'Bad orientation - {self.orient}')
		self.widgets[key]=w

	def link(self, config:dict):
		for k in config:
			self.widgets[k].link(config[k])
