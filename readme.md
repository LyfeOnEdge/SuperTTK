# SuperTTK<a name="mark0"></a>

***Themes don't have to be hard.***

---

- [About](#mark1)
- [Requirements](#mark2)
- [Configuring ini.json](#mark3)
- [SuperLib.widgets](#mark4)
	- [Core Functions](#mark5)
		- [bbox_to_width_and_height](#mark6)
		- [center_window](#mark7)
		- [check_in_bounds](#mark8)
		- [complex_widget_search](#mark9)
		- [copy_to_user_clipboard](#mark10)
		- [create_round_rectangle](#mark11)
		- [default_pack](#mark12)
		- [default_separator](#mark13)
		- [default_vertical_pack](#mark14)
		- [default_vertical_separator](#mark15)
		- [enable_notebook_movement](#mark16)
		- [focus_next](#mark17)
		- [force_aspect](#mark18)
		- [get_asset](#mark19)
		- [get_bundled_themes_list](#mark20)
		- [get_generated_font_images_lookup](#mark21)
		- [get_local_appdata_folder](#mark22)
		- [get_themes_folder](#mark23)
		- [open_link](#mark24)
		- [recursive_widget_search](#mark25)
		- [run_cl](#mark26)
	- [Core Widgets](#mark27)
		- [MultiWidgetMixin](#mark28)
		- [SuperWidgetMixin](#mark29)
	- [Tabs](#mark30)
		- [Tab](#mark31)
		- [LauncherTab](#mark32)
		- [BrowserLauncherTab](#mark33)
		- [CommandLauncherTab](#mark34)
		- [ConsoleTab](#mark35)
		- [TableTab](#mark36)
		- [TreeTableTab](#mark37)
	- [Canvas Widgets](#mark38)
		- [ResizableCanvas](#mark39)
		- [ScrolledCanvas](#mark40)
		- [TiledCanvas](#mark41)
		- [ExampleTile](#mark42)
	- [Checkbutton Widgets](#mark43)
		- [LabeledCheckbutton](#mark44)
		- [LabeledMultiCheckbutton](#mark45)
	- [Combobox Widgets](#mark46)
		- [LabeledCombobox](#mark47)
		- [LabeledMultiCombobox](#mark48)
	- [Console Widgets](#mark49)
		- [ConsoleWidget](#mark50)
	- [Entry Widgets](#mark51)
		- [ScrolledEntry](#mark52)
		- [LabeledEntry](#mark53)
		- [LabeledMultiEntry](#mark54)
		- [LabeledButtonEntry](#mark55)
		- [PasswordEntry](#mark56)
	- [KeyPad Widgets](#mark57)
		- [KeypadButton](#mark58)
		- [BaseKeypad](#mark59)
		- [DialerKeypad](#mark60)
	- [ListBox Widgets](#mark61)
		- [ScrolledListBox](#mark62)
		- [Table](#mark63)
	- [OptionMenu Widgets](#mark64)
		- [LabeledOptionMenu](#mark65)
		- [LabeledMultiOptionMenu](#mark66)
	- [ProgressBar Widgets](#mark67)
		- [LabeledProgressbar](#mark68)
		- [LabeledMultiProgressbar](#mark69)
	- [Radiobutton Widgets](#mark70)
		- [LabeledRadiobutton](#mark71)
		- [LabeledMultiRadiobutton](#mark72)
	- [Scale Widgets](#mark73)
		- [LabeledScale](#mark74)
		- [LabeledMultiScale](#mark75)
	- [Text Widgets](#mark76)
		- [ScrolledText](#mark77)
		- [CopyBox](#mark78)
	- [Toplevel Widgets](#mark79)
		- [FocusedToplevel](#mark80)
		- [NoticeWindow](#mark81)
		- [YesNoCancelWindow](#mark82)
		- [PromptWindow](#mark83)
		- [PasswordWindow](#mark84)
		- [ListWindow](#mark85)
	- [Misc Widgets](#mark86)
		- [ToolTip](#mark87)
		- [EasySizegrip](#mark88)
- [SuperLib.utils](#mark89)
	- [Utils](#mark90)
		- [check_if_module_installed](#mark91)
		- [check_string_contains](#mark92)
		- [dummy_function](#mark93)
		- [get_friendly_time](#mark94)
		- [get_installed_packages](#mark95)
		- [get_unix_timestamp](#mark96)
		- [get_unix_timestring](#mark97)
		- [get_user_home_folder](#mark98)
		- [open_folder_in_explorer](#mark99)
		- [sort_dict_by_keys](#mark100)
		- [timer_decorator](#mark101)
	- [File Generators](#mark102)
		- [HTML_Generator](#mark103)
		- [TXT_Generator](#mark104)
		- [MD_Generator](#mark105)
	- [History Mixin](#mark106)
		- [HistoryMixin](#mark107)
	- [Color Functions](#mark108)
		- [reduce](#mark109)
		- [rgb_to_hex](#mark110)
		- [rgba_to_hex](#mark111)
		- [hex_to_rgb](#mark112)
		- [hex_to_rgba](#mark113)
		- [get_gradient](#mark114)
		- [rgb_to_scalar](#mark115)
		- [scalar_to_rgb](#mark116)
		- [linear_gradient](#mark117)
		- [get_rainbow](#mark118)
- [SuperLib.mega_widgets](#mark119)
	- [Notes MegaWidget](#mark120)
		- [NotesTab](#mark121)
	- [Conversation MegaWidget](#mark122)
		- [ConversationsTab](#mark123)
	- [Profile Management](#mark124)
		- [ProfilesSystem](#mark125)
		- [UserProfile](#mark126)
		- [get_profiles_folder](#mark127)
		- [get_profiles_list](#mark128)


---

# About<a name="mark1"></a>[^](#mark0)



SuperTTK exists because I got tired of rewriting the same code over and over for simple projects. The goal is to provide a variety of meta widgets with consistent get/set/enable/disable/destroy methods and mega-widgets that make ttk development easier and faster. Features include built-in theme support, a score of labeled and multi-widgets, tools for easy form building, a sample application demonstrating many of SuperTTK's features, a configuration file system, and much more. ![Lines of code](https://img.shields.io/tokei/lines/github/LyfeOnEdge/SuperTTK)

# Requirements<a name="mark2"></a>[^](#mark0)





# Configuring ini.json<a name="mark3"></a>[^](#mark0)



```
+--------------------+-------------------------------------------+
|        Key         |                   Value                   |
+--------------------+-------------------------------------------+
| application        | Application Name (String)                 |
| version            | Application Version (String)              |
| icon               | Application Icon Path (String)            |
| width              | Startup Window Width (Int)                |
| height             | Startup Window Height (Int)               |
| minwidth           | Window Minimum Width (Int)                |
| minheight          | Window Minimum Height (Int)               |
| scaling            | Window Scaling (Float)                    |
| scale_minsize      | Scale application Minimum Size (Boolean)  |
| scale_startsize    | Scale application Start Size (Boolean)    |
| resizable_width    | Enable Window Width Resizing (Boolean)    |
| resizable_height   | Enable Window Height Resizing (Boolean)   |
| start_maximized    | Start Window Maximized (Boolean)          |
| enable_maximized   | Enable Window Maximized (Boolean)         |
| start_fullscreen   | Start Window in Fullscreen mode (Boolean) |
| enable_fullscreen  | Enable Window Fullscreen option (Boolean) |
| enable_themes_menu | Enable Themes Dropdown (Boolean)          |
| movable_tabs       | Enable Moveable Notebook Tabs (Boolean)   |
| enable_users       | Enable a User Profiles System             |
+--------------------+-------------------------------------------+
```
# SuperLib.widgets<a name="mark4"></a>[^](#mark0)



## Core Functions<a name="mark5"></a>[^](#mark4)



### SuperLib.widgets.WidgetsCore.bbox_to_width_and_height<a name="mark6"></a>[^](#mark5)

> **Takes a bbox and converts it to a width and height tuple.**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.bbox_to_width_and_height(bbox):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.center_window<a name="mark7"></a>[^](#mark5)

> **Centers spawn window on main window. Call win.update_idletasks() on either window before calling this if said window is not yet shown.**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.center_window(main_window: tkinter.Tk, spawn_window: tkinter.Toplevel):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.check_in_bounds<a name="mark8"></a>[^](#mark5)

> **Checks if a position is within a given bounds. Pos is generally a mouse event position tuple, bounds is generally a canvas.bbox(), but a (left, top, right, bottom) tuple will work too.**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.check_in_bounds(pos: tuple, bounds: tuple):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.complex_widget_search<a name="mark9"></a>[^](#mark5)

> **A more robust version of the widget search with lists for multiple widget types found in one go**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.complex_widget_search(node_widget, widget_types_to_find: list, found_lists={}):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.copy_to_user_clipboard<a name="mark10"></a>[^](#mark5)

> **Copies a string to the user's clipboard.**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.copy_to_user_clipboard(widget, value):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.create_round_rectangle<a name="mark11"></a>[^](#mark5)

> **Draws a rounded rectangle of a given radius on a tk.canvas**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.create_round_rectangle(canvas, x1, y1, x2, y2, r=20, fill='', outline='#000000', **kwargs):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.default_pack<a name="mark12"></a>[^](#mark5)

> **Apply a consistent descending packing method.**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.default_pack(widget, bottom: bool = False):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.default_separator<a name="mark13"></a>[^](#mark5)

> **Apply a consistent horizontal separator.**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.default_separator(f: tkinter.ttk.Frame, padx: int = 35, pady=(10, 5)):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.default_vertical_pack<a name="mark14"></a>[^](#mark5)

> **Apply a consistent packing method to vertically packed widgets.**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.default_vertical_pack(widget, expand: bool = False, fill: str = 'both', padx: int = 0):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.default_vertical_separator<a name="mark15"></a>[^](#mark5)

> **Apply a consistent vertical separator.**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.default_vertical_separator(frame: tkinter.ttk.Frame, pady: int = 15, padx: int = 10):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.enable_notebook_movement<a name="mark16"></a>[^](#mark5)

> **Copyright CJB 2010-07-31: https://wiki.tcl-lang.org/page/Drag+and+Drop+Notebook+Tabs Enables Tab dragging in subsequently created notebooks. Only run this function once.**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.enable_notebook_movement(app):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.focus_next<a name="mark17"></a>[^](#mark5)

> **Forces focus to the widget after the one that triggered the event**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.focus_next(event):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.force_aspect<a name="mark18"></a>[^](#mark5)

> **Forces an inner frame to maintain an aspect ratio regardless of the outer frame's size**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.force_aspect(inner_frame: tkinter.ttk.Frame, outer_frame: tkinter.ttk.Frame, ratio=1.7777777777777777):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.get_asset<a name="mark19"></a>[^](#mark5)

> **Gets an asset from the included assets folder by relative path**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.get_asset(path, folder='C:\\Users\\arcti\\github\\SuperTTK\\SuperLib\\widgets\\../../assets'):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.get_bundled_themes_list<a name="mark20"></a>[^](#mark5)

> **None**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.get_bundled_themes_list(verbose=False):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.get_generated_font_images_lookup<a name="mark21"></a>[^](#mark5)

> **Makes a lookup for the pre-generated open-sans font monograms that ship with SuperTTK.**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.get_generated_font_images_lookup(path=None):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.get_local_appdata_folder<a name="mark22"></a>[^](#mark5)

> **Opens user's Windows home folder. Only works on Windows for obvious reasons.**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.get_local_appdata_folder():
> 	...
> ```
### SuperLib.widgets.WidgetsCore.get_themes_folder<a name="mark23"></a>[^](#mark5)

> **Gets the absolute path to the included themes folder**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.get_themes_folder():
> 	...
> ```
### SuperLib.widgets.WidgetsCore.open_link<a name="mark24"></a>[^](#mark5)

> **Opens a link in the user's default web browser. `Returns None`**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.open_link(link: str):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.recursive_widget_search<a name="mark25"></a>[^](#mark5)

> **Adds widgets of a given type to a list as it travels up, away from the root of a widget tree. This method can be slow on large widget trees but is useful for retheming tk widgets with ttk formatting on theme changes. `Returns a list of widgets`**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.recursive_widget_search(node_widget, widget_type_to_find, found_list=[]):
> 	...
> ```
### SuperLib.widgets.WidgetsCore.run_cl<a name="mark26"></a>[^](#mark5)

> **Runs something via command line. `Returns None`**
> 
> ```py
> def SuperLib.widgets.WidgetsCore.run_cl(commands: list):
> 	...
> ```
## Core Widgets<a name="mark27"></a>[^](#mark4)



### SuperLib.widgets.MultiWidget.MultiWidgetMixin<a name="mark28"></a>[^](#mark27)

> **An abstract mixin that provides a way to easily instantiate multiple of the same class of a widget and making complicated forms with simple get/set methods.**
> 
> MultiWidgets support a simple get/set system. Calling get without a configuration list returns a dict of subwidget keys mapped to the values of each subwidget's .get value. Passing a list of subwidget keys limits MultiWidgetMixin.get to said subwidgets. Subclassing a multiwidget with one or more instances of one class and then calling multiwidget.add() with different classes after is acceptable assuming the widget supports being added and .get / .set / .enable / .disable / .clear methods.
> ```py
> class MultiWidgetMixin(builtins.object):
> 	def __init__(self, widget_type, config: dict):
> 		...
> 	def add(self, parent, key, args, kwargs, widget_type=None):
> 		"""Method for adding different widgets to a multiwidget post=instantiation"""
> 	def clear(self, config: list = None):
> 		"""Pass a list of subwidgets to clear or all are set to default"""
> 	def disable(self, config: list = None):
> 		"""Pass a list of subwidgets to disable or all are disabled"""
> 	def enable(self, config: list = None):
> 		"""Pass a list of subwidgets to enable or all are enabled"""
> 	def get(self, config: list = None):
> 		"""Pass a list of widget keys to get a dict of outputs"""
> 	def set(self, config: dict):
> 		"""Pass a map of widget keys and their values"""
> 
> ```
### SuperLib.widgets.WidgetsCore.SuperWidgetMixin<a name="mark29"></a>[^](#mark27)

> **Mixin to easily bind many of the common tkinter events.**
> 
> This class serves to add bindings for the majority of common tkinter widget events. The bindings are made in add mode to prevent previous / new bindings from causing unintended side-effects.
> ```py
> class SuperWidgetMixin(builtins.object):
> 	def __init__(self, on_mouse_enter=None, on_mouse_leave=None, on_mouse_move=None, on_mouse_wheel=None, on_left_click=None, on_middle_click=None, on_right_click=None, on_configure=None, bind_mouse_scroll=False):
> 		...
> 
> ```
## Tabs<a name="mark30"></a>[^](#mark4)



### SuperLib.widgets.Tabs.Tab<a name="mark31"></a>[^](#mark30)

> **The core Tab class.**
> 
> The notebook object can be any ttk.Notebook, automatically adds itself to its parent notebook with title being the tab label. This class may be instantiated directly and added to or subclassed based on need.
> ```py
> class Tab(tkinter.ttk.Frame):
> 	def __init__(self, notebook: tkinter.ttk.Notebook, title: str):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 
> ```
### SuperLib.widgets.Tabs.LauncherTab<a name="mark32"></a>[^](#mark30)

> **Basic Tab for launching tasks from a list.**
> 
> Performs an action on a list of options. The options argument is formatted as such: `options = {"Button Text 1": val1,"Button Text 2": val2}` Button presses will call `action(val)`
> ```py
> class LauncherTab(SuperLib.widgets.Tabs.Tab):
> 	def __init__(self, notebook: tkinter.ttk.Notebook, title: str, options: dict, action: Callable):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 
> ```
### SuperLib.widgets.Tabs.BrowserLauncherTab<a name="mark33"></a>[^](#mark30)

> **LauncherTab that opens a list of URLS/Files**
> 
> Takes a dict of button texts as keys and urls to open as values
> ```py
> class BrowserLauncherTab(SuperLib.widgets.Tabs.LauncherTab):
> 	def __init__(self, notebook: tkinter.ttk.Notebook, title: str, options: dict):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 
> ```
### SuperLib.widgets.Tabs.CommandLauncherTab<a name="mark34"></a>[^](#mark30)

> **LauncherTab that runs a list of commands**
> 
> Takes a dict of button texts as keys and command prompt commands to execute as values
> ```py
> class CommandLauncherTab(SuperLib.widgets.Tabs.LauncherTab):
> 	def __init__(self, notebook: tkinter.ttk.Notebook, title: str, options: dict):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 
> ```
### SuperLib.widgets.Tabs.ConsoleTab<a name="mark35"></a>[^](#mark30)

> **Basic console tab using a ConsoleWidget**
> 
> ```py
> class ConsoleTab(SuperLib.widgets.Tabs.Tab):
> 	def __init__(self, notebook: tkinter.ttk.Notebook, **kwargs):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 
> ```
### SuperLib.widgets.Tabs.TableTab<a name="mark36"></a>[^](#mark30)

> **Basic Table Tab**
> 
> table_contents is a dictionary whose keys map to lists with the column contents
> ```py
> class TableTab(SuperLib.widgets.Tabs.Tab):
> 	def __init__(self, notebook: tkinter.ttk.Notebook, title: str, table_contents: dict, **kw):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 
> ```
### SuperLib.widgets.Tabs.TreeTableTab<a name="mark37"></a>[^](#mark30)

> **Improved Table Tab**
> 
> table_contents is a dictionary whose keys map to list with the column contents
> ```py
> class TreeTableTab(SuperLib.widgets.Tabs.Tab):
> 	def __init__(self, notebook: tkinter.ttk.Notebook, title: str, table_contents: dict = {}, **kw):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 
> ```
## Canvas Widgets<a name="mark38"></a>[^](#mark4)



### SuperLib.widgets.ResizableCanvas.ResizableCanvas<a name="mark39"></a>[^](#mark38)

> **Resizeable Canvas**
> 
> Canvas resizes to fit frame on configure event.
> ```py
> class ResizableCanvas(tkinter.Canvas):
> 	def __init__(self, parent, **kw):
> 		...
> 	def create_arc(self, *args, **kw):
> 		"""Create arc shaped region with coordinates x1,y1,x2,y2."""
> 	def create_bitmap(self, *args, **kw):
> 		"""Create bitmap with coordinates x1,y1."""
> 	def create_image(self, *args, **kw):
> 		"""Create image item with coordinates x1,y1."""
> 	def create_line(self, *args, **kw):
> 		"""Create line with coordinates x1,y1,...,xn,yn."""
> 	def create_oval(self, *args, **kw):
> 		"""Create oval with coordinates x1,y1,x2,y2."""
> 	def create_polygon(self, *args, **kw):
> 		"""Create polygon with coordinates x1,y1,...,xn,yn."""
> 	def create_rectangle(self, *args, **kw):
> 		"""Create rectangle with coordinates x1,y1,x2,y2."""
> 	def create_round_rectangle(self, x1: float, y1: float, x2: float, y2: float, r: float = 20, fill: str = '', outline: str = '#000000', **kwargs):
> 		"""Draws a rounded rectangle of a given radius on a tk.canvas."""
> 	def create_text(self, *args, **kw):
> 		"""Create text with coordinates x1,y1."""
> 	def create_window(self, *args, **kw):
> 		"""Create window with coordinates x1,y1,x2,y2."""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def refresh(self):
> 		"""Refresh Canvas"""
> 
> ```
### SuperLib.widgets.ScrolledCanvas.ScrolledCanvas<a name="mark40"></a>[^](#mark38)

> **Resizeable, Auto-Scrollbarred Canvas**
> 
> Canvas resizes to fit frame on configure event. Canvas has automatic Scrollbars that appear when needed. Canvas background color is based on current theme. Due to how the scrolling is handled the actual Canvas is accessd via `ScrolledCanvas().canvas`.
> ```py
> class ScrolledCanvas(tkinter.ttk.Frame):
> 	def __init__(self, parent, on_mouse_enter=None, on_mouse_leave=None, on_mouse_move=None, on_mouse_wheel=None, on_left_click=None, on_middle_click=None, on_right_click=None, on_configure=None, bind_canvas_scroll=True, **kw):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def get_adjusted_y_view(self, event):
> 		"""Gets a canvas y-view adjusted based on its scrolled position"""
> 	def use_style(self, style):
> 		"""Reformat with a given ttk style. `Returns None`"""
> 
> ```
### SuperLib.widgets.ScrolledCanvas.TiledCanvas<a name="mark41"></a>[^](#mark38)

> ```py
> class TiledCanvas(SuperLib.widgets.ScrolledCanvas.ScrolledCanvas):
> 	def __init__(self, *args, tile_width=400, tile_height=100, tile_padx=5, tile_pady=5, tile_color='#424548', text_color='#CCCCCC', border_color='#000000', on_tile_left_click=None, on_tile_middle_click=None, on_tile_right_click=None, override_tile_width=False, **kw):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def get_adjusted_y_view(self, event):
> 		"""Gets a canvas y-view adjusted based on its scrolled position"""
> 	def refresh(self, event=None):
> 		"""Redraw the canvas"""
> 	def use_style(self, style):
> 		"""Reformat with a given ttk style. `Returns None`"""
> 
> ```
### SuperLib.widgets.ScrolledCanvas.ExampleTile<a name="mark42"></a>[^](#mark38)

> **An example tile for a Scrolled Canvas**
> 
> ```py
> class ExampleTile(builtins.object):
> 	def __init__(self, manager, text):
> 		...
> 	def activate(self):
> 		"""Calls the manager to activate the widget."""
> 	def deactivate(self):
> 		"""Calls the manager to deactivate the widget."""
> 	def is_in_range(self, pointer_x, pointer_y):
> 		"""Checks if the mouse pointer is in the tile."""
> 	def set_position(self, x, y):
> 		"""Sets a tiles position for the draw manager's draw method."""
> 
> ```
## Checkbutton Widgets<a name="mark43"></a>[^](#mark4)



### SuperLib.widgets.CheckbuttonWidgets.LabeledCheckbutton<a name="mark44"></a>[^](#mark43)

> **Labeled Checkbutton**
> 
> The "replace_output" keyword argument allows the user to provide a tuple of len 2 to replace the default True/False return values. The "is_child" keyword is used by the multiwidget mixin for label configuration and should probably be left alone unless you are making your own multiwidgets.
> ```py
> class LabeledCheckbutton(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Checkbutton):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str = '', replace_output: list = None, default: bool = False, is_child: bool = False, **kw):
> 		...
> 	def clear(self):
> 		"""Sets the Checkbutton to its default value, usually *False* `Returns None`"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self):
> 		"""Disable Checkbutton. `Returns None`"""
> 	def enable(self):
> 		"""Enable Checkbutton. `Returns None`"""
> 	def get(self):
> 		"""Get Checkbutton value. `Returns a Boolean unless replace_output is set`"""
> 	def set(self, val: bool):
> 		"""Set Checkbutton value. `Returns None`"""
> 
> ```
### SuperLib.widgets.CheckbuttonWidgets.LabeledMultiCheckbutton<a name="mark45"></a>[^](#mark43)

> **Labeled MultiWidget LabeledCheckbutton.**
> 
> Used when you need multiple, vertically stacked Labeled Checkbuttons
> ```py
> class LabeledMultiCheckbutton(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Frame, SuperLib.widgets.MultiWidget.MultiWidgetMixin):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, config: dict, is_child: bool = False, labelside='top'):
> 		...
> 	def add(self, parent, key, args, kwargs, widget_type=None):
> 		"""Method for adding different widgets to a multiwidget post=instantiation"""
> 	def clear(self, config: list = None):
> 		"""Pass a list of subwidgets to clear or all are set to default"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self, config: list = None):
> 		"""Pass a list of subwidgets to disable or all are disabled"""
> 	def enable(self, config: list = None):
> 		"""Pass a list of subwidgets to enable or all are enabled"""
> 	def get(self, config: list = None):
> 		"""Pass a list of widget keys to get a dict of outputs"""
> 	def set(self, config: dict):
> 		"""Pass a map of widget keys and their values"""
> 
> ```
## Combobox Widgets<a name="mark46"></a>[^](#mark4)



### SuperLib.widgets.ComboboxWidgets.LabeledCombobox<a name="mark47"></a>[^](#mark46)

> **Labeled Combobox widget**
> 
> Set custom_values keyword to "False" to disable custom user-entered values. Set the "default" keyword to the index of the value to display by default from the "values" keyword.
> ```py
> class LabeledCombobox(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Combobox):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, default: int = 0, custom_values: bool = True, values: list = (), is_child: bool = False, labelside: str = 'left'):
> 		...
> 	def clear(self):
> 		"""Sets Combobox to its default value. `Returns None`"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self):
> 		"""Disable Combobox. `Returns None`"""
> 	def enable(self):
> 		"""Enable Combobox. `Returns None`"""
> 	def get(self):
> 		"""Get Combobox value. `Returns a String`"""
> 	def set(self, val: str):
> 		"""Set Combobox value. `Returns None`"""
> 
> ```
### SuperLib.widgets.ComboboxWidgets.LabeledMultiCombobox<a name="mark48"></a>[^](#mark46)

> **Labeled MultiWidget LabeledCombobox**
> 
> Used when you need mutiple, vertically stacked Labeled Comboboxes
> ```py
> class LabeledMultiCombobox(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Frame, SuperLib.widgets.MultiWidget.MultiWidgetMixin):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, config: dict, is_child: bool = False, labelside='top'):
> 		...
> 	def add(self, parent, key, args, kwargs, widget_type=None):
> 		"""Method for adding different widgets to a multiwidget post=instantiation"""
> 	def clear(self, config: list = None):
> 		"""Pass a list of subwidgets to clear or all are set to default"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self, config: list = None):
> 		"""Pass a list of subwidgets to disable or all are disabled"""
> 	def enable(self, config: list = None):
> 		"""Pass a list of subwidgets to enable or all are enabled"""
> 	def get(self, config: list = None):
> 		"""Pass a list of widget keys to get a dict of outputs"""
> 	def set(self, config: dict):
> 		"""Pass a map of widget keys and their values"""
> 
> ```
## Console Widgets<a name="mark49"></a>[^](#mark4)



### SuperLib.widgets.ConsoleWidgets.ConsoleWidget<a name="mark50"></a>[^](#mark49)

> **Set labeltext, even if temporarily at init or the label widget will be ignored**
> 
> Used when you need to drop a console interface into an application. To write to the console call console.print(value). Pass a function as the "command" keyword argument to handle the entry input.
> ```py
> class ConsoleWidget(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Frame):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str = 'Console: ', entrylabeltext: str = 'Command: ', labelside: str = 'top', button_text: str = 'Run', is_child: bool = False, **kwargs):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def print(self, val, end: str = '\n'):
> 		"""Prints a line to the console with a customizable line ending. `Returns None`"""
> 
> ```
## Entry Widgets<a name="mark51"></a>[^](#mark4)



### SuperLib.widgets.EntryWidgets.ScrolledEntry<a name="mark52"></a>[^](#mark51)

> **Scrolled ttk.Entry with SuperWidgetMixin**
> 
> This class is here for completeness but most of the time you will want to use the ScrolledText widget. Used when you need a scrollable text entry box.
> ```py
> class ScrolledEntry(SuperLib.widgets.Scroller.Scroller, tkinter.ttk.Entry, SuperLib.widgets.WidgetsCore.SuperWidgetMixin):
> 	def __init__(self, parent, **kw):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def get(self):
> 		"""Return the text."""
> 
> ```
### SuperLib.widgets.EntryWidgets.LabeledEntry<a name="mark53"></a>[^](#mark51)

> **Labeled ttk.Entry with SuperWidgetMixin**
> 
> Used when you need a Labeled Entry
> ```py
> class LabeledEntry(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Entry, SuperLib.widgets.WidgetsCore.SuperWidgetMixin):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, command: Callable = None, default: str = '', on_keystroke: bool = False, bind_enter: bool = True, bind_escape_clear: bool = True, is_child: bool = False, min_width: int = 0, widgetargs={}, **kw):
> 		...
> 	def clear(self):
> 		"""Set Entry value to default, empty unless default set. `Returns None`"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self):
> 		"""Disable Entry. `Returns None`"""
> 	def enable(self):
> 		"""Enable Entry. `Returns None`"""
> 	def get(self):
> 		"""Get Entry value. `Returns a String`"""
> 	def set(self, val):
> 		"""Set Entry value. `Returns None`"""
> 
> ```
### SuperLib.widgets.EntryWidgets.LabeledMultiEntry<a name="mark54"></a>[^](#mark51)

> **Labeled MultiWidget LabeledEntry**
> 
> Used when you need multiple, vertically stacked Labeled Entries
> ```py
> class LabeledMultiEntry(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Frame, SuperLib.widgets.MultiWidget.MultiWidgetMixin):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, config: dict, is_child: bool = False, labelside='top'):
> 		...
> 	def add(self, parent, key, args, kwargs, widget_type=None):
> 		"""Method for adding different widgets to a multiwidget post=instantiation"""
> 	def clear(self, config: list = None):
> 		"""Pass a list of subwidgets to clear or all are set to default"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self, config: list = None):
> 		"""Pass a list of subwidgets to disable or all are disabled"""
> 	def enable(self, config: list = None):
> 		"""Pass a list of subwidgets to enable or all are enabled"""
> 	def get(self, config: list = None):
> 		"""Pass a list of widget keys to get a dict of outputs"""
> 	def set(self, config: dict):
> 		"""Pass a map of widget keys and their values"""
> 
> ```
### SuperLib.widgets.EntryWidgets.LabeledButtonEntry<a name="mark55"></a>[^](#mark51)

> **LabeledEntry with a ttk.Button on the right**
> 
> ```py
> class LabeledButtonEntry(SuperLib.widgets.EntryWidgets.LabeledEntry):
> 	def __init__(self, *args, button_text='', **kwargs):
> 		...
> 	def clear(self):
> 		"""Set Entry value to default, empty unless default set. `Returns None`"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self):
> 		"""Disable Entry. `Returns None`"""
> 	def enable(self):
> 		"""Enable Entry. `Returns None`"""
> 	def get(self):
> 		"""Get Entry value. `Returns a String`"""
> 	def set(self, val):
> 		"""Set Entry value. `Returns None`"""
> 
> ```
### SuperLib.widgets.EntryWidgets.PasswordEntry<a name="mark56"></a>[^](#mark51)

> **Username / Password Entry**
> 
> A username/password entry widget with optional password peeking. Set password_char to `''` to show password by default. The provided command will always be called with the tuple `(username_entry.get(), password_entry.get())` as the only argument even if one of the entries is disabled.
> ```py
> class PasswordEntry(tkinter.ttk.Frame):
> 	def __init__(self, *args, instruction_text: str = '', username_text: str = 'Username: ', username_enabled: bool = True, password_text: str = 'Password: ', password_enabled: bool = True, button_text: str = 'Submit', command=<built-in function print>, password_char: str = '*', peek_enabled: bool = True, invert_peek_colors: bool = False, **kwargs):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def on_peek_press(self, event=None):
> 		"""Show the contents of the password entry while it is being pressed"""
> 	def on_peek_release(self, event=None):
> 		"""Rehide the contents of the password entry"""
> 	def on_submit(self, event=None):
> 		"""Calls the provided "command" function with the contents of the entry box. `Returns None`"""
> 
> ```
## KeyPad Widgets<a name="mark57"></a>[^](#mark4)



### SuperLib.widgets.KeyPadWidgets.KeypadButton<a name="mark58"></a>[^](#mark57)

> **Base Keypad Button**
> 
> Keypad button that automatically packs itself based on given coordinates. This object is not usually directly instantiated.
> ```py
> class KeypadButton(tkinter.ttk.Button):
> 	def __init__(self, frame, value, coords, callback):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 
> ```
### SuperLib.widgets.KeyPadWidgets.BaseKeypad<a name="mark59"></a>[^](#mark57)

> **Base Keypad Class**
> 
> Either instantiate directly with a custom layout or subclass with each subclass supplying a custom layout for more keypads. Subclass KeypadButton and supply the class as the "button_type" kwarg for custom buttons.
> ```py
> class BaseKeypad(tkinter.ttk.Frame):
> 	def __init__(self, layout, callback, button_class=<class 'SuperLib.widgets.KeyPadWidgets.KeypadButton'>, *args, **kwargs):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 
> ```
### SuperLib.widgets.KeyPadWidgets.DialerKeypad<a name="mark60"></a>[^](#mark57)

> **Phone Dialer Keypad**
> 
> Example 12-button keypad, subclass BaseKeypad and supply a custom layout for more keypads.
> ```py
> class DialerKeypad(SuperLib.widgets.KeyPadWidgets.BaseKeypad):
> 	def __init__(self, callback, *args, **kwargs):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 
> ```
## ListBox Widgets<a name="mark61"></a>[^](#mark4)



### SuperLib.widgets.ListBoxWidgets.ScrolledListBox<a name="mark62"></a>[^](#mark61)

> **Scrolled Listbox with SuperWidget mixin**
> 
> ```py
> class ScrolledListBox(SuperLib.widgets.Scroller.Scroller, tkinter.Listbox, SuperLib.widgets.WidgetsCore.SuperWidgetMixin):
> 	def __init__(self, parent, **kw):
> 		...
> 	def activate(self, index):
> 		"""Activate item identified by INDEX."""
> 	def curselection(self):
> 		"""Return the indices of currently selected item."""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def get(self, first, last=None):
> 		"""Get list of items from FIRST to LAST (included)."""
> 
> ```
### SuperLib.widgets.ListBoxWidgets.Table<a name="mark63"></a>[^](#mark61)

> **Listboxes bound to scroll in union. Additional bindings will be needed in order to handle clicking.**
> 
> Tested on Mac/Windows/Linux. In most cases a TreeTable widget will be superior to this.
> ```py
> class Table(tkinter.ttk.Frame):
> 	def __init__(self, *args, min_column_width: int = 100, start_column_width: int = 100, on_selection=None, **kw):
> 		...
> 	def build(self, contents: dict):
> 		"""Rebuild the table"""
> 	def clear(self):
> 		"""Clears the table"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def get(self):
> 		"""Gets the currently selected items from the table. `Returns a List of Strings`"""
> 	def use_style(self, style: tkinter.ttk.Style):
> 		"""Update to match supplied ttk.Style object. `Returns None`"""
> 
> ```
## OptionMenu Widgets<a name="mark64"></a>[^](#mark4)



### SuperLib.widgets.OptionMenuWidgets.LabeledOptionMenu<a name="mark65"></a>[^](#mark64)

> **Labeled OptionMenu widget**
> 
> ```py
> class LabeledOptionMenu(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.OptionMenu):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, options: list, default: int = 0, is_child: bool = False):
> 		...
> 	def clear(self):
> 		"""Sets OptionMenu to its default value. `Returns None`"""
> 	def destroy(self):
> 		"""Destroy this widget and its associated variable."""
> 	def disable(self):
> 		"""Disable OptionMenu. `Returns None`"""
> 	def enable(self):
> 		"""Enable OptionMenu. `Returns None`"""
> 	def get(self):
> 		"""Get OptionMenu value. `Returns a String`"""
> 	def set(self, val):
> 		"""Set OptionMenu value. `Returns None`"""
> 	def set_menu(self, default=None, *values):
> 		"""Build a new menu of radiobuttons with *values and optionally
>         a default value."""
> 
> ```
### SuperLib.widgets.OptionMenuWidgets.LabeledMultiOptionMenu<a name="mark66"></a>[^](#mark64)

> **Labeled MultiWidget LabeledOptionMenu**
> 
> ```py
> class LabeledMultiOptionMenu(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Frame, SuperLib.widgets.MultiWidget.MultiWidgetMixin):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, config: dict, is_child: bool = False, labelside='top'):
> 		...
> 	def add(self, parent, key, args, kwargs, widget_type=None):
> 		"""Method for adding different widgets to a multiwidget post=instantiation"""
> 	def clear(self, config: list = None):
> 		"""Pass a list of subwidgets to clear or all are set to default"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self, config: list = None):
> 		"""Pass a list of subwidgets to disable or all are disabled"""
> 	def enable(self, config: list = None):
> 		"""Pass a list of subwidgets to enable or all are enabled"""
> 	def get(self, config: list = None):
> 		"""Pass a list of widget keys to get a dict of outputs"""
> 	def set(self, config: dict):
> 		"""Pass a map of widget keys and their values"""
> 
> ```
## ProgressBar Widgets<a name="mark67"></a>[^](#mark4)



### SuperLib.widgets.ProgressbarWidgets.LabeledProgressbar<a name="mark68"></a>[^](#mark67)

> **Labeled Progressbar**
> 
> ```py
> class LabeledProgressbar(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Progressbar):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, orient='horizontal', labelside='left', is_child=False, default: float = 0, **kw):
> 		...
> 	def clear(self):
> 		"""Sets Progresbar progress to its default value `Returns None`"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self):
> 		"""Enable Progresbar. `Returns None`"""
> 	def enable(self):
> 		"""Disable Progresbar. `Returns None`"""
> 	def get(self):
> 		"""Set Progresbar progress. `Returns None`"""
> 	def link(self, widget):
> 		"""Easily link to other widgets, sets the progressbar var to the passed widget's var. `Returns None`"""
> 	def set(self, val):
> 		"""Get Progresbar progress. `Returns a String`"""
> 	def start(self, interval=None):
> 		"""Begin autoincrement mode: schedules a recurring timer event
>         that calls method step every interval milliseconds.
> 
>         interval defaults to 50 milliseconds (20 steps/second) if omitted."""
> 	def step(self, amount=None):
> 		"""Increments the value option by amount.
> 
>         amount defaults to 1.0 if omitted."""
> 	def stop(self):
> 		"""Stop autoincrement mode: cancels any recurring timer event
>         initiated by start."""
> 
> ```
### SuperLib.widgets.ProgressbarWidgets.LabeledMultiProgressbar<a name="mark69"></a>[^](#mark67)

> **Labeled MultiWidget LabeledProgressbar**
> 
> ```py
> class LabeledMultiProgressbar(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Frame, SuperLib.widgets.MultiWidget.MultiWidgetMixin):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, config: dict, is_child: bool = False, labelside='top', orient='horizontal'):
> 		...
> 	def add(self, parent: tkinter.ttk.Frame, key: str, args, kwargs, widget_type=None):
> 		"""Overrides MultiWidgetMixin to deal with vertical orientation `Returns None`"""
> 	def clear(self, config: list = None):
> 		"""Pass a list of subwidgets to clear or all are set to default"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self, config: list = None):
> 		"""Pass a list of subwidgets to disable or all are disabled"""
> 	def enable(self, config: list = None):
> 		"""Pass a list of subwidgets to enable or all are enabled"""
> 	def get(self, config: list = None):
> 		"""Pass a list of widget keys to get a dict of outputs"""
> 	def link(self, config: dict):
> 		"""Link to other widgets with a dict of subwidget keys to link to `Returns None`"""
> 	def set(self, config: dict):
> 		"""Pass a map of widget keys and their values"""
> 
> ```
## Radiobutton Widgets<a name="mark70"></a>[^](#mark4)



### SuperLib.widgets.RadiobuttonWidgets.LabeledRadiobutton<a name="mark71"></a>[^](#mark70)

> **Labeled Radiobutton widget**
> 
> ```py
> class LabeledRadiobutton(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Frame):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, options: list = [], default: int = 0, is_child: bool = False):
> 		...
> 	def clear(self):
> 		"""Sets Radiobutton to its default value. `Returns None`"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self):
> 		"""Enable Radiobutton. `Returns None`"""
> 	def enable(self):
> 		"""Disable Radiobutton. `Returns None`"""
> 	def get(self):
> 		"""Get Radiobutton value. `Returns a Bool`"""
> 	def set(self, val: bool):
> 		"""Set Radiobutton value. `Returns None`"""
> 
> ```
### SuperLib.widgets.RadiobuttonWidgets.LabeledMultiRadiobutton<a name="mark72"></a>[^](#mark70)

> **Labeled MultiWidget LabeledRadiobutton**
> 
> ```py
> class LabeledMultiRadiobutton(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Frame, SuperLib.widgets.MultiWidget.MultiWidgetMixin):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, config: dict, is_child: bool = False, labelside='top'):
> 		...
> 	def add(self, parent, key, args, kwargs, widget_type=None):
> 		"""Method for adding different widgets to a multiwidget post=instantiation"""
> 	def clear(self, config: list = None):
> 		"""Pass a list of subwidgets to clear or all are set to default"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self, config: list = None):
> 		"""Pass a list of subwidgets to disable or all are disabled"""
> 	def enable(self, config: list = None):
> 		"""Pass a list of subwidgets to enable or all are enabled"""
> 	def get(self, config: list = None):
> 		"""Pass a list of widget keys to get a dict of outputs"""
> 	def set(self, config: dict):
> 		"""Pass a map of widget keys and their values"""
> 
> ```
## Scale Widgets<a name="mark73"></a>[^](#mark4)



### SuperLib.widgets.ScaleWidgets.LabeledScale<a name="mark74"></a>[^](#mark73)

> **Labeled Scale**
> 
> ```py
> class LabeledScale(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Scale):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, command: Callable = None, default: float = 0, orient: bool = 'horizontal', is_child: bool = False, from_=0, to=100, **kwargs):
> 		...
> 	def clear(self):
> 		"""Sets Scale to its default value. `Returns None`"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self):
> 		"""Enable Scale. `Returns None`"""
> 	def enable(self):
> 		"""Disable Scale. `Returns None`"""
> 	def get(self):
> 		"""Get Scale value. `Returns a Float`"""
> 	def set(self, val):
> 		"""Set Scale value. `Returns None`"""
> 
> ```
### SuperLib.widgets.ScaleWidgets.LabeledMultiScale<a name="mark75"></a>[^](#mark73)

> **Labeled MultiWidget Labeled Scale**
> 
> ```py
> class LabeledMultiScale(SuperLib.widgets.Labeler.Labeler, tkinter.ttk.Frame, SuperLib.widgets.MultiWidget.MultiWidgetMixin):
> 	def __init__(self, parent: tkinter.ttk.Frame, labeltext: str, config: dict, is_child: bool = False, labelside='top', orient='horizontal', command=None):
> 		...
> 	def add(self, parent, key, args, kwargs, widget_type=None):
> 		"""Override MultiWidgetMixin for vertical orientation"""
> 	def clear(self, config: list = None):
> 		"""Pass a list of subwidgets to clear or all are set to default"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def disable(self, config: list = None):
> 		"""Pass a list of subwidgets to disable or all are disabled"""
> 	def enable(self, config: list = None):
> 		"""Pass a list of subwidgets to enable or all are enabled"""
> 	def get(self, config: list = None):
> 		"""Pass a list of widget keys to get a dict of outputs"""
> 	def set(self, config: dict):
> 		"""Pass a map of widget keys and their values"""
> 
> ```
## Text Widgets<a name="mark76"></a>[^](#mark4)



### SuperLib.widgets.TextWidgets.ScrolledText<a name="mark77"></a>[^](#mark76)

> **Scrolled Textbox**
> 
> Scrolled SuperWidget Text. Configure text by passing the `textkw` argument as a dict formatted like a standard kwarg dict.
> ```py
> class ScrolledText(SuperLib.widgets.Scroller.Scroller, tkinter.Text, SuperLib.widgets.WidgetsCore.SuperWidgetMixin):
> 	def __init__(self, parent, **kw):
> 		...
> 	def clear(self):
> 		"""Empties the text box. `Returns None`"""
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def edit_undo(self):
> 		"""Undoes the last edit action
> 
>         If the undo option is true. An edit action is defined
>         as all the insert and delete commands that are recorded
>         on the undo stack in between two separators. Generates
>         an error when the undo stack is empty. Does nothing
>         when the undo option is false
>         """
> 	def get(self, start='1.0', end='end'):
> 		"""Returns the contents of the text box with optional start/end kwargs. `Returns a String`"""
> 	def get_cursor(self):
> 		"""Get the current location of the cursor. `Returns None`"""
> 	def select_all(self, event=None):
> 		"""Selects all text. `Returns None`"""
> 	def set(self, val):
> 		"""Sets the text. `Returns a String`"""
> 	def window_create(self, index, cnf={}, **kw):
> 		"""Create a window at INDEX."""
> 
> ```
### SuperLib.widgets.TextWidgets.CopyBox<a name="mark78"></a>[^](#mark76)

> **Scrolled Text with "Copy tp Clipboard" Button**
> 
> A widget with a scrolled textbox and button that copies the textbox contents to the user's clipboard. Useful for form output, etc.
> ```py
> class CopyBox(tkinter.ttk.Frame):
> 	def __init__(self, parent: tkinter.ttk.Frame, **kw):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 
> ```
## Toplevel Widgets<a name="mark79"></a>[^](#mark4)



### SuperLib.widgets.ToplevelWidgets.FocusedToplevel<a name="mark80"></a>[^](#mark79)

> **Base Focused Toplevel Class**
> 
> Window that takes focus and center's itself on the current window. Used as a base class for other windows.
> ```py
> class FocusedToplevel(tkinter.Toplevel):
> 	def __init__(self, *args, title=None, window=None, **kwargs):
> 		...
> 	def destroy(self):
> 		...
> 	def iconify(self):
> 		"""Display widget as icon."""
> 	def iconmask(self, bitmap=None):
> 		"""Set mask for the icon bitmap of this widget. Return the
>         mask if None is given."""
> 
> ```
### SuperLib.widgets.ToplevelWidgets.NoticeWindow<a name="mark81"></a>[^](#mark79)

> **Provides the user with a notice.**
> 
> `button_action` can call a function to help with determining acceptance vs. the user hitting the exit button.
> ```py
> class NoticeWindow(SuperLib.widgets.ToplevelWidgets.FocusedToplevel):
> 	def __init__(self, *args, text=None, button_text='Continue', button_action=None, **kwargs):
> 		...
> 	def destroy(self):
> 		...
> 	def iconify(self):
> 		"""Display widget as icon."""
> 	def iconmask(self, bitmap=None):
> 		"""Set mask for the icon bitmap of this widget. Return the
>         mask if None is given."""
> 
> ```
### SuperLib.widgets.ToplevelWidgets.YesNoCancelWindow<a name="mark82"></a>[^](#mark79)

> **Provides the user with a yes/no/cancel option.**
> 
> `no_destroy` can be set to `True` to allow the window to remain open after a selection is made.
> ```py
> class YesNoCancelWindow(SuperLib.widgets.ToplevelWidgets.FocusedToplevel):
> 	def __init__(self, *args, text: str = None, yes_enabled: bool = True, on_yes=None, yes_text: str = 'Yes', no_enabled: bool = True, on_no=None, no_text: str = 'No', cancel_enabled: bool = True, on_cancel=None, cancel_text: str = 'Cancel', no_destroy: bool = False, **kwargs):
> 		...
> 	def destroy(self):
> 		...
> 	def iconify(self):
> 		"""Display widget as icon."""
> 	def iconmask(self, bitmap=None):
> 		"""Set mask for the icon bitmap of this widget. Return the
>         mask if None is given."""
> 
> ```
### SuperLib.widgets.ToplevelWidgets.PromptWindow<a name="mark83"></a>[^](#mark79)

> **Prompts the user for a text input**
> 
> `no_destroy` can be set to `True` to allow the window to remain open after a selection is made, useful for informing the user a string input was invalid via setting label_var.
> ```py
> class PromptWindow(SuperLib.widgets.ToplevelWidgets.FocusedToplevel):
> 	def __init__(self, *args, text: str = 'Enter Text:', on_yes=None, yes_text: str = 'Continue', on_cancel=None, cancel_text: str = 'Cancel', bind_enter: bool = True, no_destroy: bool = False, **kwargs):
> 		...
> 	def destroy(self):
> 		...
> 	def iconify(self):
> 		"""Display widget as icon."""
> 	def iconmask(self, bitmap=None):
> 		"""Set mask for the icon bitmap of this widget. Return the
>         mask if None is given."""
> 
> ```
### SuperLib.widgets.ToplevelWidgets.PasswordWindow<a name="mark84"></a>[^](#mark79)

> **Password Entry window.**
> 
> Demo Password Entry Window, you will want to copy the source for this widget and rewrite it.
> ```py
> class PasswordWindow(SuperLib.widgets.ToplevelWidgets.FocusedToplevel):
> 	def __init__(self, window=None, **kwargs):
> 		...
> 	def destroy(self):
> 		...
> 	def iconify(self):
> 		"""Display widget as icon."""
> 	def iconmask(self, bitmap=None):
> 		"""Set mask for the icon bitmap of this widget. Return the
>         mask if None is given."""
> 
> ```
### SuperLib.widgets.ToplevelWidgets.ListWindow<a name="mark85"></a>[^](#mark79)

> **Window to select an option from a Scrolled Listbox**
> 
> ```py
> class ListWindow(SuperLib.widgets.ToplevelWidgets.FocusedToplevel):
> 	def __init__(self, *args, options: list, text: str = 'Select Item:', on_yes=None, yes_text: str = 'Continue', on_cancel=None, cancel_text: str = 'Cancel', no_destroy: bool = False, select_mode: str = 'single', **kwargs):
> 		...
> 	def destroy(self):
> 		...
> 	def iconify(self):
> 		"""Display widget as icon."""
> 	def iconmask(self, bitmap=None):
> 		"""Set mask for the icon bitmap of this widget. Return the
>         mask if None is given."""
> 
> ```
## Misc Widgets<a name="mark86"></a>[^](#mark4)



### SuperLib.widgets.ToolTip.ToolTip<a name="mark87"></a>[^](#mark86)

> **Easy ToolTip**
> 
> Easily show theme-friendly tooltip. Currently only left and right align are supported.
> ```py
> class ToolTip(SuperLib.widgets.ToolTip.ToolTipBase):
> 	def __init__(self, tipwidget, text: str, align='left'):
> 		...
> 
> ```
### SuperLib.widgets.SizegripWidgets.EasySizegrip<a name="mark88"></a>[^](#mark86)

> **Sizegrip widget with bindings**
> 
> Automatically packs self and binds mouse presses for systems that don't bind automatically.
> ```py
> class EasySizegrip(tkinter.ttk.Sizegrip):
> 	def __init__(self, *args, **kwargs):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 
> ```
# SuperLib.utils<a name="mark89"></a>[^](#mark0)



## Utils<a name="mark90"></a>[^](#mark89)



### SuperLib.utils.utils.check_if_module_installed<a name="mark91"></a>[^](#mark90)

> **Indicates if a packages is installed. `Returns a Boolean`**
> 
> ```py
> def SuperLib.utils.utils.check_if_module_installed(package):
> 	...
> ```
### SuperLib.utils.utils.check_string_contains<a name="mark92"></a>[^](#mark90)

> **Returns `(True, char_index)` if any character from the list exists in the string otherwise returns `(False, None)`**
> 
> ```py
> def SuperLib.utils.utils.check_string_contains(string: str, contains_list: tuple):
> 	...
> ```
### SuperLib.utils.utils.dummy_function<a name="mark93"></a>[^](#mark90)

> **Dummy function that nicely prints out any passed args and kwargs. `Returns None`**
> 
> ```py
> def SuperLib.utils.utils.dummy_function(*args, **kwargs):
> 	...
> ```
### SuperLib.utils.utils.get_friendly_time<a name="mark94"></a>[^](#mark90)

> **Gets a time string in one of several modes. Modes: `all, time, date, nice_date`. `Returns a String`**
> 
> ```py
> def SuperLib.utils.utils.get_friendly_time(timestamp, mode='all'):
> 	...
> ```
### SuperLib.utils.utils.get_installed_packages<a name="mark95"></a>[^](#mark90)

> **Get an alphabetized list of available packages. `Returns a List`**
> 
> ```py
> def SuperLib.utils.utils.get_installed_packages():
> 	...
> ```
### SuperLib.utils.utils.get_unix_timestamp<a name="mark96"></a>[^](#mark90)

> **Get a unix timestamp. `Returns a Float`**
> 
> ```py
> def SuperLib.utils.utils.get_unix_timestamp():
> 	...
> ```
### SuperLib.utils.utils.get_unix_timestring<a name="mark97"></a>[^](#mark90)

> **Get a unix timestring. `Returns a String`**
> 
> ```py
> def SuperLib.utils.utils.get_unix_timestring():
> 	...
> ```
### SuperLib.utils.utils.get_user_home_folder<a name="mark98"></a>[^](#mark90)

> **Cross-platform function to get a user's home folder**
> 
> ```py
> def SuperLib.utils.utils.get_user_home_folder():
> 	...
> ```
### SuperLib.utils.utils.open_folder_in_explorer<a name="mark99"></a>[^](#mark90)

> **Cross-platform way to open a folder in the default file manager for a system**
> 
> ```py
> def SuperLib.utils.utils.open_folder_in_explorer(path):
> 	...
> ```
### SuperLib.utils.utils.sort_dict_by_keys<a name="mark100"></a>[^](#mark90)

> **Sorts a dictionary by its keys**
> 
> ```py
> def SuperLib.utils.utils.sort_dict_by_keys(source: dict, reverse: bool = False):
> 	...
> ```
### SuperLib.utils.utils.timer_decorator<a name="mark101"></a>[^](#mark90)

> **Decorator to add timing to a function**
> 
> ```py
> def SuperLib.utils.utils.timer_decorator(proc):
> 	...
> ```
## File Generators<a name="mark102"></a>[^](#mark89)



### SuperLib.utils.HTML_Generator.HTML_Generator<a name="mark103"></a>[^](#mark102)

> ```py
> class HTML_Generator(builtins.object):
> 	def __init__(self, indent='\t'):
> 		...
> 	def add_body_line(self, text=''):
> 		...
> 	def add_bold(self, text=''):
> 		...
> 	def add_center(self, text=''):
> 		...
> 	def add_comment(self, text):
> 		...
> 	def add_div(self, text=''):
> 		...
> 	def add_divider(self):
> 		...
> 	def add_paragraph(self, text=''):
> 		...
> 	def assemble(self):
> 		...
> 	def end_bold(self):
> 		...
> 	def end_center(self):
> 		...
> 	def end_div(self):
> 		...
> 	def end_paragraph(self):
> 		...
> 	def get_indent(self, offset=0):
> 		...
> 	def save(self, path):
> 		...
> 	def start_bold(self, text=''):
> 		...
> 	def start_center(self, text=''):
> 		...
> 	def start_div(self, text=''):
> 		...
> 	def start_paragraph(self, text=''):
> 		...
> 
> ```
### SuperLib.utils.TXT_Generator.TXT_Generator<a name="mark104"></a>[^](#mark102)

> ```py
> class TXT_Generator(builtins.object):
> 	def __init__(self, ):
> 		...
> 	def add_body_line(self, text=''):
> 		...
> 	def add_divider(self):
> 		...
> 	def assemble(self):
> 		...
> 	def save(self, path):
> 		...
> 
> ```
### SuperLib.utils.MD_Generator.MD_Generator<a name="mark105"></a>[^](#mark102)

> ```py
> class MD_Generator(builtins.object):
> 	def __init__(self, title=None, footnote_title='Notes:', footnote_heading_level=2, numbered_toc=False):
> 		...
> 	def add_blockquote(self, text, end='\n\n'):
> 		...
> 	def add_bold(self, text, end='\n\n'):
> 		...
> 	def add_bold_italic(self, text, end='\n'):
> 		...
> 	def add_break(self):
> 		...
> 	def add_code_block(self, text, lang='', end='\n'):
> 		...
> 	def add_heading_1(self, text, **kwargs):
> 		...
> 	def add_heading_2(self, text, **kwargs):
> 		...
> 	def add_heading_3(self, text, **kwargs):
> 		...
> 	def add_heading_4(self, text, **kwargs):
> 		...
> 	def add_heading_5(self, text, **kwargs):
> 		...
> 	def add_heading_6(self, text, **kwargs):
> 		...
> 	def add_horizontal_rule(self):
> 		...
> 	def add_italic(self, text, end='\n'):
> 		...
> 	def add_link(self, link, text=None, tooltip=None):
> 		...
> 	def add_multi_blockquote(self, texts):
> 		...
> 	def add_ordered_list(self, texts, indent=0):
> 		...
> 	def add_paragraph(self, text, end='\n\n'):
> 		...
> 	def add_to_ordered_list(self, index, text, indent=0):
> 		...
> 	def add_to_unordered_list(self, text, indent=0):
> 		...
> 	def add_toc(self, title, end='\n\n'):
> 		...
> 	def add_unordered_list(self, texts, indent=0):
> 		...
> 	def assemble(self):
> 		...
> 	def decrease_toc_depth(self):
> 		...
> 	def get_prefix(self):
> 		...
> 	def increase_toc_depth(self):
> 		...
> 	def insert_footnote(self, text):
> 		...
> 	def save(self, path):
> 		...
> 	def set_slogan(self, slogan):
> 		...
> 
> ```
## History Mixin<a name="mark106"></a>[^](#mark89)



### SuperLib.utils.History.HistoryMixin<a name="mark107"></a>[^](#mark106)

> **Abstract mixin to add history-tracking to an application**
> 
> This object is meant to be used as a mixin rather than instantiated directly most of the time.
> ```py
> class HistoryMixin(builtins.object):
> 	def __init__(self, data):
> 		...
> 	def add_history(self, data):
> 		...
> 	def clear_history(self, data):
> 		...
> 	def get_history_uid(self):
> 		...
> 	def redo(self):
> 		...
> 	def undo(self):
> 		...
> 
> ```
## Color Functions<a name="mark108"></a>[^](#mark89)



### SuperLib.utils.color.reduce<a name="mark109"></a>[^](#mark108)

> **Limits a val to a range of 0 to 255**
> 
> ```py
> def SuperLib.utils.color.reduce(in_value: int, maxval: int = 255):
> 	...
> ```
### SuperLib.utils.color.rgb_to_hex<a name="mark110"></a>[^](#mark108)

> **Converts an rgb tuple to hex**
> 
> ```py
> def SuperLib.utils.color.rgb_to_hex(rgb: tuple):
> 	...
> ```
### SuperLib.utils.color.rgba_to_hex<a name="mark111"></a>[^](#mark108)

> **Converts an rgba tuple to rgba hex**
> 
> ```py
> def SuperLib.utils.color.rgba_to_hex(rgba: tuple):
> 	...
> ```
### SuperLib.utils.color.hex_to_rgb<a name="mark112"></a>[^](#mark108)

> **Converts hex to rgb tuple**
> 
> ```py
> def SuperLib.utils.color.hex_to_rgb(hex: str):
> 	...
> ```
### SuperLib.utils.color.hex_to_rgba<a name="mark113"></a>[^](#mark108)

> **Tries to convert rgba hex to rgba, on failure converts rgb hex to rgb and sets a full opacity**
> 
> ```py
> def SuperLib.utils.color.hex_to_rgba(hex: str):
> 	...
> ```
### SuperLib.utils.color.get_gradient<a name="mark114"></a>[^](#mark108)

> **Generates a gradient with a given number of steps**
> 
> ```py
> def SuperLib.utils.color.get_gradient(steps: int):
> 	...
> ```
### SuperLib.utils.color.rgb_to_scalar<a name="mark115"></a>[^](#mark108)

> **Converts an rgb itterable to scalar list**
> 
> ```py
> def SuperLib.utils.color.rgb_to_scalar(rgb: tuple):
> 	...
> ```
### SuperLib.utils.color.scalar_to_rgb<a name="mark116"></a>[^](#mark108)

> **Converts rgb scalar to rgb list**
> 
> ```py
> def SuperLib.utils.color.scalar_to_rgb(rgb: tuple):
> 	...
> ```
### SuperLib.utils.color.linear_gradient<a name="mark117"></a>[^](#mark108)

> **Generates a linear gradient between two colors, accepts html hex or rgb formats**
> 
> ```py
> def SuperLib.utils.color.linear_gradient(start_hex: str = '#000000', finish_hex: str = '#FFFFFF', n: int = 10):
> 	...
> ```
### SuperLib.utils.color.get_rainbow<a name="mark118"></a>[^](#mark108)

> **Generates a rainbow with a given number of steps. Steps must be divisible by 4)**
> 
> ```py
> def SuperLib.utils.color.get_rainbow(steps: int):
> 	...
> ```
# SuperLib.mega_widgets<a name="mark119"></a>[^](#mark0)



## Notes MegaWidget<a name="mark120"></a>[^](#mark119)



### SuperLib.mega_widgets.notes.NotesTab<a name="mark121"></a>[^](#mark120)

> ```py
> class NotesTab(SuperLib.widgets.Tabs.Tab):
> 	def __init__(self, notebook, app):
> 		...
> 	def copy_note(self, note):
> 		...
> 	def delete_note(self, note):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def export_note_html(self, note):
> 		...
> 	def export_note_json(self, note):
> 		...
> 	def export_note_markdown(self, note):
> 		...
> 	def export_note_text(self, note):
> 		...
> 	def load_notes(self):
> 		...
> 	def make_new_note(self, title):
> 		...
> 	def new_note(self, event=None):
> 		...
> 	def on_toplevel_destroy(self, *args):
> 		"""Function for toplevels to call on no / cancel"""
> 	def reload_notes(self):
> 		...
> 	def rename_note(self, note):
> 		...
> 	def start_new_note(self, title=None):
> 		...
> 
> ```
## Conversation MegaWidget<a name="mark122"></a>[^](#mark119)



### SuperLib.mega_widgets.chat.ConversationsTab<a name="mark123"></a>[^](#mark122)

> ```py
> class ConversationsTab(SuperLib.widgets.Tabs.Tab):
> 	def __init__(self, notebook, app):
> 		...
> 	def copy_conversation(self, conversation):
> 		...
> 	def delete_conversation(self, conversation):
> 		...
> 	def destroy(self):
> 		"""Destroy this and all descendants widgets."""
> 	def export_conversation_html(self, conversation):
> 		...
> 	def export_conversation_json(self, conversation):
> 		...
> 	def export_conversation_markdown(self, conversation):
> 		...
> 	def export_conversation_text(self, conversation):
> 		...
> 	def get_cached_icon(self, size, color, char):
> 		...
> 	def get_user_icon(self, user):
> 		...
> 	def load_conversations(self):
> 		...
> 	def make_new_conversation(self, title):
> 		...
> 	def new_conversation(self, event=None):
> 		...
> 	def on_toplevel_destroy(self, *args):
> 		"""Function for toplevels to call on no / cancel"""
> 	def reload_conversations(self):
> 		...
> 	def rename_conversation(self, conversation):
> 		...
> 	def start_new_conversation(self, title=None):
> 		...
> 
> ```
## Profile Management<a name="mark124"></a>[^](#mark119)



### SuperLib.utils.ProfilesSystem.ProfilesSystem<a name="mark125"></a>[^](#mark124)

> ```py
> class ProfilesSystem(builtins.object):
> 	def __init__(self, select_profile_actions: list = [], profiles_dir: str = 'C:\\Users\\arcti\\github\\SuperTTK\\Profiles', handle_duplicates: bool = True):
> 		...
> 	def add_select_profile_action(self, action):
> 		"""Add an action to the profile switch actions"""
> 	def add_select_profile_actions(self, actions: list):
> 		"""Add a list of actions to the profile switch actions"""
> 	def check_if_name_exists_in_profiles(self, name: str, profiles: list = None):
> 		"""Check if a name exists in a list of profiles, if no list is provided uses the list of all profiles. `Returns a Bool`"""
> 	def clear_select_profile_actions(self, new: list = []):
> 		"""Clear out the profile switch actions, optionally replacing them with new ones"""
> 	def create_profile(self, name: str):
> 		"""Creates a profile with a given name. `Raises ValueError` if the profile name already exists. `Returns a UserProfile`"""
> 	def get_last_used_profile(self, profiles: list = None):
> 		"""Returns the most recently accessed profile"""
> 	def handle_duplicate_profile_names(self, name: str):
> 		"""Makes profile names unique if they have identical names. The most recently accessed profile (according to the file json) keeps its name untouched. `Returns None`"""
> 	def select_profile(self, profile: SuperLib.utils.ProfilesSystem.UserProfile):
> 		"""Change the currently selected profile"""
> 	def select_profile_by_username(self, name: str):
> 		...
> 	def sort_profiles_by_accessed(self, profiles: list = None):
> 		"""Sort a list of profiles by last accessed, if no list is provided returns a sorted list of all profiles in the system. `Returns a List`"""
> 
> ```
### SuperLib.utils.ProfilesSystem.UserProfile<a name="mark126"></a>[^](#mark124)

> **A class to represent a User / User's Preferences**
> 
> Must pass a unique username and a unique identifier for new profile.
> ```py
> class UserProfile(builtins.object):
> 	def __init__(self, path, username: str = None, atomic: str = None):
> 		...
> 	def clear_preferences(self, preferences: list = None):
> 		...
> 	def get_preference(self, key: str):
> 		...
> 	def load(self):
> 		...
> 	def save(self):
> 		...
> 	def set_preference(self, key: str, value: str):
> 		...
> 	def set_username(self, name: str):
> 		...
> 
> ```
### SuperLib.utils.ProfilesSystem.get_profiles_folder<a name="mark127"></a>[^](#mark126)

> **Gets the absolute path to the included profiles folder. `Returns a String`**
> 
> ```py
> def SuperLib.utils.ProfilesSystem.get_profiles_folder():
> 	...
> ```
### SuperLib.utils.ProfilesSystem.get_profiles_list<a name="mark128"></a>[^](#mark126)

> **Gets a list of profile files at a given path. `Returns a List of Path strings`**
> 
> ```py
> def SuperLib.utils.ProfilesSystem.get_profiles_list(path='../../Profiles', verbose=False):
> 	...
> ```
