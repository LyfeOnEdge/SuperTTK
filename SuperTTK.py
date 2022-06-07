#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
if sys.hexversion < 0x03060000:
	sys.exit('Python 3.6 or greater is required to run this program.')

import json
import os
import typing
import platform
import subprocess
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from typing import Callable
from math import sin

if __name__=='__main__':
	from widgets.WidgetsCore import default_separator, default_pack, default_vertical_separator,\
		default_vertical_pack, copy_to_user_clipboard, recursive_widget_search
	from widgets.CheckbuttonWidgets import LabeledCheckbutton, LabeledMultiCheckbutton
	from widgets.ComboboxWidgets import LabeledCombobox, LabeledMultiCombobox
	from widgets.OptionMenuWidgets import LabeledOptionMenu, LabeledMultiOptionMenu
	from widgets.EntryWidgets import LabeledEntry, LabeledMultiEntry, LabeledButtonEntry
	from widgets.ProgressbarWidgets import LabeledProgressbar, LabeledMultiProgressbar
	from widgets.ScaleWidgets import LabeledScale, LabeledMultiScale
	from widgets.RadiobuttonWidgets import LabeledRadiobutton, LabeledMultiRadiobutton
	from widgets.TextWidgets import ScrolledText, CopyBox
	from widgets.ConsoleWidgets import ConsoleWidget
	from widgets.Tabs import Tab, LauncherTab, BrowserLauncherTab, CommandLauncherTab, ConsoleTab
	from widgets.ToolTip import ToolTip
	from utils.utils import run_cl, open_link
	from utils.lorem_ipsum import get_lorem_paragraphs
else:
	from .widgets.WidgetsCore import default_separator, default_pack, default_vertical_separator,\
		default_vertical_pack, copy_to_user_clipboard, recursive_widget_search
	from .widgets.CheckbuttonWidgets import LabeledCheckbutton, LabeledMultiCheckbutton
	from .widgets.ComboboxWidgets import LabeledCombobox, LabeledMultiCombobox
	from .widgets.OptionMenuWidgets import LabeledOptionMenu, LabeledMultiOptionMenu
	from .widgets.EntryWidgets import LabeledEntry, LabeledMultiEntry, LabeledButtonEntry
	from .widgets.ProgressbarWidgets import LabeledProgressbar, LabeledMultiProgressbar
	from .widgets.ScaleWidgets import LabeledScale, LabeledMultiScale
	from .widgets.RadiobuttonWidgets import LabeledRadiobutton, LabeledMultiRadiobutton
	from .widgets.TextWidgets import ScrolledText, CopyBox
	from .widgets.ConsoleWidgets import ConsoleWidget
	from .widgets.Tabs import Tab, LauncherTab, BrowserLauncherTab, CommandLauncherTab, ConsoleTab
	from .widgets.ToolTip import ToolTip
	from .utils.utils import run_cl, open_link
	from .utils.lorem_ipsum import get_lorem_paragraphs

def get_themes_folder(): return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'themes')

class _AbstractAppMixin: #Non-functional code, etc
	def __init__(self, ini_data: dict):
		self.ini_data = ini_data
		self.app_name = ini_data.get('application')
		self.version = ini_data.get('version')
		self.version_name = '{} Version {}'.format(self.app_name, self.version)
		self.os = platform.system()
		self.os_version = platform.version()
		print(self.version_name)
		print('Using Python {}.{}'.format(*sys.version_info[:2]))
		print('Using tkinter version {}'.format(tk.Tcl().eval('info patchlevel')))
		
class App(_AbstractAppMixin): #Main Application Object
	def __init__(self, ini_file:str): #ini_file is the path to an ini.json file
		with open(ini_file) as f: _AbstractAppMixin.__init__(self, json.load(f))
		self.scaling = self.ini_data['scaling']
		self.window_start_width = int(self.ini_data['width'] * self.scaling)
		self.window_start_height = int(self.ini_data['height'] * self.scaling)
		self.window_min_width=int(self.ini_data.get('minwidth', 300)*self.scaling)
		self.window_min_height=int(self.ini_data.get('minheight', 300)*self.scaling)
		self.window = tk.Tk()
		self.window.tk.call('tk', 'scaling', self.ini_data['scaling'])
		self.notebook = ttk.Notebook(self.window)
		self.notebook.pack(fill=tk.BOTH, expand=tk.YES)
		menubar = tk.Menu(self.window)
		self.window.configure(menu=menubar)
		'''Theme'''
		print(f"Themes folder located at {get_themes_folder()}")
		self.themes = self.get_themes_list(verbose=True)
		print(f"Loading bundled themes...")
		for t in self.themes: self.window.tk.call('source', t)
		print(f"Finished loading bundled themes...")
		self.style = ttk.Style()

		self.available_themes = self.style.theme_names()
		print(f"Available themes: {json.dumps(self.available_themes, indent=4)}")
		self.theme_menu = tk.Menu(menubar, tearoff=tk.OFF)
		for t in self.available_themes:
			self.theme_menu.add_command(label=t, command=lambda t=t:self.theme_use(t))
		menubar.add_cascade(label="Themes",menu=self.theme_menu)
		'''Window Geometry'''
		self.window.geometry(f"{self.window_start_width}x{self.window_start_height}")
		self.window.title(self.version_name)
		self.window.minsize(
			width=self.window_min_width,
			height=self.window_min_height
		)
		resizable_width = self.ini_data.get('resizable_width', True)
		resizable_height = self.ini_data.get('resizable_height', True)
		self.window.resizable(resizable_width,resizable_height)
		if resizable_width and resizable_height:
			if self.ini_data.get('start_maximized', False):
				self.window.state('zoomed') #Maximize window
		self.theme_use('winnative')

	def theme_use(self, theme:str):
		self.style.theme_use(theme)

		#Configure the 'header' labels for widgets
		fnt = tkFont.nametofont('TkDefaultFont').actual()
		fnt = (fnt['family'],fnt['size'],'bold')
		self.style.configure('Bold.TLabel', font=fnt)

		text_bg = self.style.lookup('TEntry', 'fieldbackground') or "white"
		text_fg = self.style.lookup('TEntry', 'foreground') or "black"
		widgets = [] #List to populate with scrolled text boxes
		recursive_widget_search(self.notebook, ScrolledText, widgets)
		for w in widgets: w.configure(bg=text_bg, fg=text_fg)

	def get_themes_list(self, verbose = False):
		themes = []
		for entry in os.scandir(get_themes_folder()):
			if entry.is_file():
				if entry.path.endswith('.tcl'):
					themes.append(entry.path)
		if verbose:
			print(f"Found {len(themes)} bundled themes: {json.dumps(themes, indent=4)}")
		return themes

	def copy_to_user_clipboard(self, val:str):
		self.window.clipboard_clear()
		self.window.clipboard_append(val)
		
	def mainloop(self):
		self.window.mainloop()

if __name__ == '__main__':
	print("SuperTTK Example / Test")

	links = {
				'Google':'https://www.google.com/',
				'YouTube':'http://youtu.be/',
				'Gmail':'https://www.gmail.com/',
			}
	apps = {
				"System Info" : ["C:\Windows\System32\msinfo32.exe"],
				"Winver" : ["C:\Windows\System32\winver.exe"],
				"Task Manager" : ["C:\Windows\System32\Taskmgr.exe"] #Fails on some systems      
			}

	class TextBoxTestTab(Tab):
		def __init__(self, notebook:ttk.Notebook):
			Tab.__init__(self, notebook, 'AutoScrollbarredTextbox')
			text = ScrolledText(self)
			text.pack(fill='both', expand=True, side=tk.TOP)
			text.insert('1.0', get_lorem_paragraphs(1000))

	class FormWidgetDemoTab(Tab):
		def __init__(self, notebook:ttk.Notebook):
			Tab.__init__(self, notebook, 'Form Widgets')
			
			self.entry = LabeledEntry(self, "Labeled Entry")
			default_pack(self.entry)
			entry_config = {
				'Entry 1':([],{'default':''}),
				'Entry 2':([],{'default':"Always 2 except when it's not..."}),
				'Entry 3':([],{'default':'101010000100101'}),
				'Entry 4':([],{'default':''}),
			}
			self.entries = LabeledMultiEntry(self, "Labeled Multi Entry", entry_config)
			default_pack(self.entries)
			default_separator(self)

			self.option_menu = LabeledOptionMenu(self, "Labeled Option Menu", ["Option 1", "Option 2"])
			default_pack(self.option_menu)
			option_menu_config = {
				'Menu 1':([['Option A','Option B']],{}),
				'Menu 2':([['ALPHA','BRAVO']],{'default':1}),
				'Menu 3':([['A','B','C','D','E']],{'default':4}),
			}
			self.option_menus = LabeledMultiOptionMenu(self, "Labeled Multi Option Menu", option_menu_config)
			default_pack(self.option_menus)
			default_separator(self)

			self.check_button = LabeledCheckbutton(self,"Labeled Check Button",buttontext="Button Text",replace_output=["Unchecked", "Checked"],default=True)
			default_pack(self.check_button)
			check_buttons_config = {
				'Int Button':([],{'buttontext':'This button will return an int','replace_output':[0,1]}),
				'Bool Button':([],{'buttontext':'This button will return a bool','default':True,'replace_output':[False,True]}),
				'String Button':([],{'buttontext':'This button will return a string','replace_output':['Unchecked','Checked']}),
			}
			self.check_buttons = LabeledMultiCheckbutton(self,'Labeled Check Buttons',check_buttons_config)
			default_pack(self.check_buttons)
			default_separator(self)

			run_button = ttk.Button(self, command=self.on_button_click, text="Run Test")
			default_pack(run_button)

			self.copy_box = CopyBox(self)
			default_pack(self.copy_box)

		def on_button_click(self, event=None):
			entry_value = self.entry.get(); self.entry.clear()
			entries_value = json.dumps(self.entries.get(), indent=4); self.entries.clear()
			option_value = self.option_menu.get(); self.option_menu.clear()
			options_value = json.dumps(self.option_menus.get(), indent=4); self.option_menus.clear()
			check_value = self.check_button.get(); self.check_button.clear()
			checks_value = json.dumps(self.check_buttons.get(), indent=4); self.check_buttons.clear()
			self.copy_box.set("Entry Value: {}\nMulti Entry Value: {}\nOption Value: {}\nMulti Option Value: {}\nCheck Value: {}\nMulti Check Value: {}".format(
				entry_value,entries_value,option_value,options_value,check_value,checks_value
			))

	class LoadingBarDemo(Tab):
		def __init__(self, notebook:ttk.Notebook):
			Tab.__init__(self, notebook, 'Bars & Scales')
			self.progress_bar = LabeledProgressbar(self, 'Labeled Progress Bar')
			default_pack(self.progress_bar)
			self.slider = LabeledScale(self, 'Labeled Scale',default=50)
			# self.progress_bar.set(self.slider.get())
			self.progress_bar.link(self.slider)
			default_pack(self.slider)
			default_separator(self)
			
			progress_config = {'A':([],{}),'B':([],{}),'C':([],{}),'D':([],{}),}
			self.progress_bars = LabeledMultiProgressbar(self, 'Labeled Progress Bars', progress_config)
			default_pack(self.progress_bars)
			slider_options = {'A':([],{'default':0}),'B':([],{'default':25}),'C':([],{'default':50}),'D':([],{'default':75})}
			self.sliders = LabeledMultiScale(self, 'Labeled Scales', slider_options)
			default_pack(self.sliders)
			self.progress_bars.link(self.sliders.widgets)
			# self.progress_bars.set(self.sliders.get())
			default_separator(self)

			vertical_slider_frame = ttk.Frame(self)
			vertical_slider_frame.pack(fill='x',expand=tk.NO,side=tk.TOP,padx=10,pady=(0,10))
			
			self.v_progress_bar = LabeledProgressbar(vertical_slider_frame,'VBar',orient=tk.VERTICAL)
			default_vertical_pack(self.v_progress_bar)
			self.v_slider = LabeledScale(vertical_slider_frame,'VScl',orient=tk.VERTICAL,from_=100,to=0,default=10)
			self.v_progress_bar.link(self.v_slider)
			default_vertical_pack(self.v_slider)
			default_vertical_separator(vertical_slider_frame)
			
			v_keys = ['E','F','G','H','I','J','K','L','M','N','O','P','Q']
			v_progress_options = {}
			v_slider_options = {}
			for k in v_keys:
				v_progress_options[k]=([],{})
				v_slider_options[k]=([],{'from_':100,'to':0,'default':50+30*sin(v_keys.index(k)/1.9)})
			self.v_progress_bars = LabeledMultiProgressbar(vertical_slider_frame,'Labeled Vertical Progress Bars',v_progress_options,orient=tk.VERTICAL)
			default_vertical_pack(self.v_progress_bars, expand=True)
			self.v_sliders = LabeledMultiScale(vertical_slider_frame,'Labeled Vertical Scales',v_slider_options,orient=tk.VERTICAL)
			default_vertical_pack(self.v_sliders, expand=True, padx=(20,0))
			self.v_progress_bars.link(self.v_sliders.widgets)
			default_separator(self)

			self.smooth_val = 0.
			def update_smooth():
				self.smooth_val += 1
				self.determinate_smooth_loading_bar.set(self.smooth_val%100)
				self.after(10,update_smooth)
			self.determinate_smooth_loading_bar = LabeledProgressbar(self,' Smooth')
			self.after(0,update_smooth)
			default_pack(self.determinate_smooth_loading_bar)
			
			self.stepped_val = 0.
			def update_stepped():
				self.stepped_val += 6
				self.determinate_stepped_loading_bar.set(self.stepped_val%100)
				self.after(400,update_stepped)
			self.after(0,update_stepped)
			self.determinate_stepped_loading_bar = LabeledProgressbar(self,' Stepped',labelside=tk.RIGHT)
			default_pack(self.determinate_stepped_loading_bar)
			default_separator(self)

			self.indeterminate_loading_bar = LabeledProgressbar(self,' Indeterminate',labelside=tk.TOP,mode='indeterminate')
			self.indeterminate_loading_bar.start()
			default_pack(self.indeterminate_loading_bar)

			self.looped_val = 0.
			def update_looped():
				self.looped_val += 1.1
				mod_val = self.looped_val%100
				self.indeterminate_loading_looped_bar.set(mod_val)
				self.indeterminate_loading_looped_bar.label.configure(text=f' Indeterminate Looped: {str(mod_val)[:4]}%')
				self.after(22,update_looped)
			self.after(0,update_looped)
			self.indeterminate_loading_looped_bar = LabeledProgressbar(self,' Indeterminate Looped',labelside=tk.BOTTOM,mode='indeterminate')
			self.indeterminate_loading_looped_bar.label.configure(anchor="center")
			default_pack(self.indeterminate_loading_looped_bar)

	class ComboRadioTab(Tab):
		def __init__(self, notebook:ttk.Notebook, ):
			Tab.__init__(self, notebook, 'Radios & Combos')
			self.box = LabeledCombobox(self, 'Labeled Combobox', values=('A', 'B'), default=0)
			default_pack(self.box)
			conf = {
				'Box 1':([],{'values':('C', 'D'),'default':0}),
				'Box 2':([],{'values':('E', 'F'),'default':1}),
				'Box 3':([],{'values':('G', 'H'),'default':0}),
			}
			self.boxes = LabeledMultiCombobox(self,'Labeled Multi Combobox',config=conf)
			default_pack(self.boxes)
			default_separator(self)

			options = ['Option 1', 'Option 2', 'Option 3']
			self.radio = LabeledRadiobutton(self, 'Labeled Radiobuttons', options, 0)
			default_pack(self.radio)

			conf = {
				'Radios 1':([['Option 4','Option 5','Option 6']],{'default':1}),
				'Radios 2':([['Option 7','Option 8','Option 9']],{'default':2}),
			}
			self.radios = LabeledMultiRadiobutton(self, 'Labeled Multi Radiobuttons', config=conf)
			default_pack(self.radios)
			default_separator(self)

			run_button = ttk.Button(self, command=self.on_button_click, text="Run Test")
			default_pack(run_button)

			self.copy_box = CopyBox(self)
			default_pack(self.copy_box)

		def on_button_click(self, event=None):
			box_value = self.box.get(); self.box.clear()
			boxes_value = json.dumps(self.boxes.get(), indent=4); self.boxes.clear()
			radio_value = self.radio.get(); self.radio.clear()
			radios_value = json.dumps(self.radios.get(), indent=4); self.radios.clear()
			self.copy_box.set("Combobox Value: {}\nMulti Combobox Value: {}\nRadio Value: {}\nRadios Value: {}".format(
				box_value, boxes_value, radio_value, radios_value
			))

	class ToolTipTab(Tab):
		def __init__(self, notebook:ttk.Notebook, ):
			Tab.__init__(self, notebook, 'Tooltips')
			header = ttk.Frame(self)
			header.pack(fill='x',expand=False,side=tk.TOP)
			self.entry_x = LabeledEntry(header,labeltext='Width',default=5)
			self.entry_y = LabeledEntry(header,labeltext='Height',default=5)
			button = ttk.Button(header,text='Rebuild',command=self.remake)
			for w in (self.entry_x,self.entry_y,button):
				w.pack(fill='both',expand='true',side=tk.LEFT)
			self.container = None #placeholder for ttk frame
			
		def remake(self,evt=None):
			if self.container: self.container.destroy()
			self.container = ttk.Frame(self)
			self.container.pack(fill='both',expand=True,side=tk.TOP,padx=5,pady=5)
			width = self.entry_x.get()
			try:
				width = int(width)
			except:
				self.entry_x.set('Err')
				return
			height = self.entry_y.get()
			try:
				height = int(height)
			except:
				self.entry_y.set('Err')
				return
			for y in range(height):
				f = ttk.Frame(self.container)
				f.pack(fill='both',expand='true',side=tk.TOP)
				for x in range(width):
					val = width*y+x
					val = f"00{val}" if val < 10 else (f"0{val}" if val < 100 else val)
					b = ttk.Button(f,text=val,padding=0,width=0,command=lambda val=val:print(f"Pressed {val}"))
					b.pack(fill='both',expand='true',side=tk.LEFT)
					ToolTip(b, f'Tooltip for button {val}')

	'''Example Implementation'''
	class ExampleApp(App):
		def __init__(self):
			App.__init__(self, "ini.json")
			self.tooltip_demp = ToolTipTab(self.notebook)
			self.loading_bar = LoadingBarDemo(self.notebook)
			self.console_tab = ConsoleTab(self.notebook)
			self.console_tab.console.command=self.console_tab.console.print
			self.textbox_tab = TextBoxTestTab(self.notebook)
			self.links_tab = BrowserLauncherTab(self.notebook, "Quick Links", links)
			self.apps_tab = CommandLauncherTab(self.notebook, "Applications", apps)
			self.form_tab = FormWidgetDemoTab(self.notebook)
			self.combo_tab = ComboRadioTab(self.notebook)
			
			self.theme_use('black') #Do this last to apply theme to text boxes

	app = ExampleApp()
	app.mainloop()