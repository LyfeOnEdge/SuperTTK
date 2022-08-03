import os
import platform
import subprocess
import sys
import time
import json
import webbrowser
import tkinter as tk
from tkinter import ttk

from .MultiWidget import MultiWidgetMixin

WINDOWS_SYMBOL = "⊞"
ASSETS_REL_PATH = "../../assets"
ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), ASSETS_REL_PATH)


def get_asset(path, folder=ASSETS_FOLDER):
    """Gets an asset from the included assets folder by relative path"""
    return os.path.join(folder, path)

def get_themes_folder():
    """Gets the absolute path to the included themes folder"""
    return os.path.abspath(os.path.join(ASSETS_FOLDER,"themes"))

def get_bundled_themes_list(verbose=False):
    def determine_theme(fp):
        return fp.endswith(".tcl") and not fp.endswith("pkgIndex.tcl")

    themes = []
    for entry in os.scandir(get_themes_folder()):
        if entry.is_file():
            if determine_theme(entry.path):
                themes.append(entry.path)
        elif entry.is_dir():
            for subentry in os.scandir(entry.path):
                if determine_theme(subentry.path):
                    themes.append(subentry.path)
    if verbose:
        print(f"Found {len(themes)} bundled themes: {json.dumps(themes, indent=4)}")
    return themes



def force_aspect(inner_frame:ttk.Frame, outer_frame:ttk.Frame, ratio=(16 / 9)):
    """Forces an inner frame to maintain an aspect ratio regardless of the outer frame's size"""

    def force_ratio(event):
        w = event.width
        h = int(event.width / ratio)
        if h > event.height:
            h = event.height
            w = int(event.height * ratio)
        inner_frame.place(
            in_=outer_frame,
            relx=0.5,
            rely=0.5,
            x=-0.5 * float(w),
            y=-0.5 * float(h),
            width=w,
            height=h,
        )

    outer_frame.bind("<Configure>", force_ratio)


def center_window(main_window:tk.Tk, spawn_window:tk.Toplevel):
    """Centers spawn window on main window. Call win.update_idletasks() on either window before calling this if said window is not yet shown."""
    pos_x, width = main_window.winfo_x(), main_window.winfo_width()
    pos_y, height = main_window.winfo_y(), main_window.winfo_height()
    width2, height2 = spawn_window.winfo_width(), spawn_window.winfo_height()
    spawn_window.geometry(
        "+%d+%d" % (pos_x + (width - width2) / 2, pos_y + (height - height2) / 2)
    )


def focus_next(event):
    """Forces focus to the widget after the one that triggered the event"""
    event.widget.tk_focusNext().focus()


def default_separator(f: ttk.Frame, padx:int=35, pady=(10, 5)):
    """Apply a consistent horizontal separator."""
    ttk.Separator(f, orient="horizontal").pack(fill="x", padx=padx, pady=pady)


def default_pack(widget, bottom:bool=False):
    """Apply a consistent descending packing method."""
    widget.pack(fill="x", expand=False, side=tk.TOP, padx=5, pady=(0, 5 * bottom))


def default_vertical_separator(frame: ttk.Frame, pady:int=15, padx:int=10):
    """Apply a consistent vertical separator."""
    ttk.Separator(frame, orient="vertical").pack(
        fill="y", padx=padx, pady=pady, expand=False, side=tk.LEFT
    )


def default_vertical_pack(widget, expand:bool=False, fill:str=tk.BOTH, padx:int=0):
    """Apply a consistent packing method to vertically packed widgets."""
    widget.pack(fill=fill, expand=expand, side=tk.LEFT, padx=padx)


def copy_to_user_clipboard(widget, value):
    """Copies a string to the user's clipboard."""
    widget.clipboard_clear()
    widget.clipboard_append(value)


def check_in_bounds(pos:tuple, bounds:tuple):
    """Checks if a position is within a given bounds. Pos is generally a mouse event position tuple, bounds is generally a canvas.bbox(), but a (left, top, right, bottom) tuple will work too."""
    x, y = pos
    lb, tb, rb, bb = bounds
    return all((x > lb, x < rb, y > tb, y < bb))


def get_generated_font_images_lookup(path=None):
    """Makes a lookup for the pre-generated open-sans font monograms that ship with SuperTTK."""
    path = path or os.path.join(ASSETS_FOLDER, "generated")
    fonts = {}
    for entry in os.scandir(path):
        if entry.is_file():
            if entry.path.endswith(".png"):
                char, size, color = entry.name[:-4].split("_")
                size = int(size)
                if not size in fonts:
                    fonts[size] = {}
                if not color in fonts[size]:
                    fonts[size][color] = {}
                fonts[size][color][char] = entry.path
    return fonts


def bbox_to_width_and_height(bbox):
    """Takes a bbox and converts it to a width and height tuple."""
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def recursive_widget_search(node_widget, widget_type_to_find, found_list=[]):
    """Adds widgets of a given type to a list as it travels up, away from the root of a widget tree. This method can be slow on large widget trees but is useful for retheming tk widgets with ttk formatting on theme changes. `Returns a list of widgets`"""
    for w in node_widget.winfo_children():
        if isinstance(w, widget_type_to_find):
            found_list.append(w)
        else:
            recursive_widget_search(w, widget_type_to_find, found_list)
    return found_list  # The only time this return is ever used is at the end of the first call


def complex_widget_search(node_widget, widget_types_to_find: list, found_lists={}):
    """A more robust version of the widget search with lists for multiple widget types found in one go"""
    if not found_lists:
        for w in widget_types_to_find:
            found_lists[w] = []
    for w in node_widget.winfo_children():
        for wt in widget_types_to_find:
            if isinstance(w, wt):
                if not found_lists.get(wt):
                    found_lists[wt] = []
                found_lists[wt].append(w)
        complex_widget_search(w, widget_types_to_find, found_lists)
    return found_lists  # The only time this return is ever used is at the end of the first call


def run_cl(commands: list):
    """Runs something via command line. `Returns None`"""
    subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def open_link(link: str):
    """Opens a link in the user's default web browser. `Returns None`"""
    print(f"Opening {link} in default web browser")
    webbrowser.open_new_tab(link)


def get_local_appdata_folder():
    """Opens user's Windows home folder. Only works on Windows for obvious reasons."""
    return os.path.expandvars("%LOCALAPPDATA%")


def enable_notebook_movement(app):
    """Copyright CJB 2010-07-31: https://wiki.tcl-lang.org/page/Drag+and+Drop+Notebook+Tabs Enables Tab dragging in subsequently created notebooks. Only run this function once."""
    tcl_configuration = """
    namespace eval tabdrag {}
    bind TNotebook <Destroy> {+tabdrag::destroy %W}
    bind TNotebook <Button-1> {+tabdrag::click %W %x %y}
    bind TNotebook <ButtonRelease-1> {+tabdrag::release %W %x %y}
    bind TNotebook <B1-Motion> {+tabdrag::move %W %x %y}

    proc ::tabdrag::destroy {win} {
      variable winstate;

      array unset winstate ?,$win
    }

    proc ::tabdrag::click {win x y} {
      variable winstate;

      set what [$win identify tab $x $y]
      if { $what eq "" || [$win index end] <= 1} {
           return;
         }

      set winstate(x,$win) $x
      set winstate(t,$win) [lindex [$win tabs] $what]
      set winstate(e,$win) 0
    }

    proc ::tabdrag::release {win x y} {
      variable winstate;

      array unset winstate ?,$win
    }

    proc ::tabdrag::move {win x y} {
      variable winstate;

      if { ![info exists winstate(x,$win)] || ![info exists winstate(t,$win)] || $winstate(t,$win) eq "" } {
           return;
         }

      set where [$win identify tab $x $y]
      if { [info exists winstate(a,$win)] } {
           if { $x < $winstate(a,$win) && $where < $winstate(i,$win) } {
                unset -nocomplain winstate(a,$win) winstate(i,$win) winstate(j,$win)
              } elseif { $x > $winstate(a,$win) && $where > $winstate(i,$win) } {
                unset -nocomplain winstate(a,$win) winstate(i,$win) winstate(j,$win)
              }
         }
      if { $where ne "" } {
           set what [lindex [$win tabs] $where]
         } else {
           set what ""
         }
      if { $what eq $winstate(t,$win) } {
           return;
         }
      if { $what eq "" } {
           # Not over a tab - check to see if we're before or after where we started
           if { $winstate(e,$win) } {
                return;
              }
           set winstate(e,$win) 1
           if { $x < $winstate(x,$win) } {
                $win insert 0 $winstate(t,$win)
              } else {
                $win insert end $winstate(t,$win)
              }
           #unset -nocomplain winstate(j,$win) winstate(a,$win) winstate(i,$win)
           set winstate(x,$win) $x
         } else {
           set winstate(e,$win) 0
           if { [info exists winstate(j,$win)] && $what eq $winstate(j,$win) } {
                if { (($x > $winstate(x,$win) && $x > $winstate(a,$win)) || ($x < $winstate(x,$win) && $x < $winstate(a,$win))) } {
                     return;# avoid stuttering when jumping a bigger tab
                   }
              }
           $win insert $what $winstate(t,$win)
           set winstate(j,$win) $what
           set winstate(a,$win) $x
           set winstate(i,$win) $where
         }
    }
    """
    app.window.tk.eval(tcl_configuration)


def create_round_rectangle(
    canvas, x1, y1, x2, y2, r=20, fill="", outline="#000000", **kwargs
):
    """Draws a rounded rectangle of a given radius on a tk.canvas"""
    x1r = x1 + r
    x2mr = x2 - r
    y1r = y1 + r
    y2mr = y2 - r

    points = (
        x1r,
        y1,
        x1r,
        y1,
        x2mr,
        y1,
        x2mr,
        y1,
        x2,
        y1,
        x2,
        y1r,
        x2,
        y1r,
        x2,
        y2mr,
        x2,
        y2mr,
        x2,
        y2,
        x2mr,
        y2,
        x2mr,
        y2,
        x1r,
        y2,
        x1r,
        y2,
        x1,
        y2,
        x1,
        y2mr,
        x1,
        y2mr,
        x1,
        y1r,
        x1,
        y1r,
        x1,
        y1,
    )
    return canvas.create_polygon(
        points,
        **kwargs,
        smooth=True,
        outline=outline,
        fill=fill,
    )


class SuperWidgetMixin:
    """Mixin to easily bind many of the common tkinter events."""

    __desc__ = """This class serves to add bindings for the majority of common tkinter widget events. The bindings are made in add mode to prevent previous / new bindings from causing unintended side-effects."""

    def __init__(
        self,
        on_mouse_enter=None,
        on_mouse_leave=None,
        on_mouse_move=None,
        on_mouse_wheel=None,
        on_left_click=None,
        on_middle_click=None,
        on_right_click=None,
        on_configure=None,
        bind_mouse_scroll=False,
    ):
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_leave = on_mouse_leave
        self.on_mouse_move = on_mouse_move
        self.on_left_click = on_left_click
        self.on_middle_click = on_middle_click
        self.on_right_click = on_right_click
        self.on_mouse_wheel = on_mouse_wheel
        self.on_configure = on_configure
        self.bind_mouse_scroll = bind_mouse_scroll
        self.bind("<Enter>", self._on_mouse_enter, add="+")
        self.bind("<Leave>", self._on_mouse_leave, add="+")
        self.bind("<Motion>", self._on_mouse_move, add="+")
        self.bind("<Button-1>", self._on_left_click, add="+")
        self.bind("<Button-2>", self._on_middle_click, add="+")
        self.bind("<Button-3>", self._on_right_click, add="+")
        self.bind("<Configure>", self._on_configure, add="+")
        self.bind("<MouseWheel>", self._on_mouse_wheel, add="+")

    def _on_mouse_enter(self, event):
        if self.on_mouse_enter:
            self.on_mouse_enter(event)

    def _on_mouse_leave(self, event):
        if self.on_mouse_leave:
            self.on_mouse_leave(event)

    def _on_mouse_move(self, event):
        if self.on_mouse_move:
            self.on_mouse_move(event)

    def _on_mouse_wheel(self, event):
        if self.on_mouse_wheel:
            self.on_mouse_wheel(event)
        if self.bind_mouse_scroll:
            _on_mousewheel(event, self)

    def _on_left_click(self, event):
        x = event.x
        if self.on_left_click:
            self.on_left_click(event)

    def _on_middle_click(self, event):
        if self.on_middle_click:
            self.on_middle_click(event)

    def _on_right_click(self, event):
        if self.on_right_click:
            self.on_right_click(event)

    def _on_configure(self, event=None):
        if self.on_configure:
            self.on_configure(w, h)


CORE_FUNCTIONS = [
    bbox_to_width_and_height,
    center_window,
    check_in_bounds,
    complex_widget_search,
    copy_to_user_clipboard,
    create_round_rectangle,
    default_pack,
    default_separator,
    default_vertical_pack,
    default_vertical_separator,
    enable_notebook_movement,
    focus_next,
    force_aspect,
    get_asset,
    get_bundled_themes_list,
    get_generated_font_images_lookup,
    get_local_appdata_folder,
    get_themes_folder,
    open_link,
    recursive_widget_search,
    run_cl,
]

CORE_OBJECTS = [MultiWidgetMixin, SuperWidgetMixin]
