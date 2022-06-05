import tkinter as tk
from tkinter import ttk
from .Labeler import Labeler
from .MultiWidget import MultiWidgetMixin

class LabeledCombobox(Labeler, ttk.Combobox):
	def __init__(
			self,parent:ttk.Frame,labeltext:str,default:int=0,\
			custom_values:bool=True,values:list=(),is_child:bool=False,
			labelside=tk.LEFT
		):
		self.var = tk.StringVar()
		self.default = values[default] if any(values) else ''
		self.var.set(self.default)
		self.is_child = is_child
		Labeler.__init__(self,parent,labeltext,labelside=labelside,header=not is_child)
		ttk.Combobox.__init__(self, self.frame, textvariable=self.var)
		ttk.Combobox.pack(self,fill='x',expand=False,side=tk.TOP)
		self['values']=values
		#Var to preserve custom values on enable / disable
		self._state = 'normal' if custom_values else 'readonly'
		
	def disable(self): self['state']=tk.DISABLED
	def enable(self): self['state']=self._state
	def get(self): return self.var.get()
	def set(self, val:str): self.var.set(val)
	def clear(self): self.var.set(self.default)

class LabeledMultiCombobox(Labeler, ttk.Frame, MultiWidgetMixin):
	def __init__(self,parent:ttk.Frame,labeltext:str,config:dict,is_child:bool=False,labelside=tk.TOP):
		Labeler.__init__(self,parent,labeltext,labelside=labelside,header=not is_child)
		ttk.Frame.__init__(self, self.frame)
		ttk.Frame.pack(self,fill='both',expand=True,side=tk.TOP)
		MultiWidgetMixin.__init__(self, LabeledCombobox,config)
		self.is_child = is_child