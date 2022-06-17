import os
import platform
import subprocess
import sys
import time
import webbrowser
import tkinter as tk
from tkinter import ttk


def timer_decorator(proc):
    def t(*args, **kw):
        start = time.time()
        res = proc(*args, **kw)
        stop = time.time()
        print("%r  %2.2f ms" % (proc.__name__, (stop - start) * 1000))
        return res

    return t


# Apply a consistent separator
def default_separator(f: ttk.Frame, padx=35, pady=(10, 5)):
    ttk.Separator(f, orient="horizontal").pack(fill="x", padx=padx, pady=pady)


# apply a consistent packing method
def default_pack(widget, bottom=False):
    widget.pack(fill="x", expand=False, side=tk.TOP, padx=5, pady=(0, 5 * bottom))


# Apply a consistent vertical separator
def default_vertical_separator(f: ttk.Frame, pady=15, padx=10):
    ttk.Separator(f, orient="vertical").pack(
        fill="y", padx=padx, pady=pady, expand=False, side=tk.LEFT
    )


# apply a consistent packing method to vertical widgets
def default_vertical_pack(widget, expand=False, fill="both", padx=0):
    widget.pack(fill=fill, expand=expand, side=tk.LEFT, padx=padx)


def copy_to_user_clipboard(widget, value):
    widget.clipboard_clear()
    widget.clipboard_append(value)


def recursive_widget_search(node_widget, widget_type_to_find, found_list=[]):
    """
    Adds widgets of a given type to a list as it travels up, away from the root of a widget tree.
    This method can be slow on large widget trees but is useful for retheming tk widgets with
    ttk formatting on theme changes
    """
    for w in node_widget.winfo_children():
        if isinstance(w, widget_type_to_find):
            found_list.append(w)
        else:
            recursive_widget_search(w, widget_type_to_find, found_list)
    return found_list  # The only time this return is ever used is at the end of the first call


def reduce(v):
    return max(0, min(v, 255))


def rgb_to_hex(rgb):
    return "#{0:02x}{1:02x}{2:02x}".format(
        reduce(rgb[0]), reduce(rgb[1]), reduce(rgb[2])
    )


def rgba_to_hex(rgba):
    return "#{0:02x}{1:02x}{2:02x}{3:02x}".format(
        reduce(rgba[0]), reduce(rgba[1]), reduce(rgba[2]), reduce(rgba[3])
    )


def hex_to_rgb(hex):
    return [int(hex[i : i + 2], 16) for i in range(1, 6, 2)]


def hex_to_rgba(hex):
    try:
        return [int(hex[i : i + 2], 16) for i in range(1, 8, 2)]
    except ValueError as e:
        rgba = hex_to_rgb(hex)
        rgba.append(255)
        return rgba


def get_gradient(steps):
    return [
        rgb_to_hex(v) for v in reversed(linear_gradient("#FFFFFF", "#000000", steps))
    ]


def rgb_to_scalar(list):
    return [int(x / 255.0) for x in list]


def scalar_to_rgb(list):
    return [int(x * 255.0) for x in list]


def linear_gradient(start_hex="#000000", finish_hex="#FFFFFF", n=10):
    s = hex_to_rgb(start_hex)
    f = hex_to_rgb(finish_hex)
    rgb = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        rgb.append([int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j])) for j in range(3)])
    return rgb


def get_rainbow(steps):
    assert steps % 4 == 0, "Steps should be divisible by 4"
    rainbow = []
    step = int(steps / 4)
    rainbow.extend(linear_gradient("#FF0000", "#FFFF00", step))
    rainbow.extend(linear_gradient("#7FFF00", "#00FF7F", step))
    rainbow.extend(linear_gradient("#00FFF", "#0000FF", step))
    rainbow.extend(linear_gradient("#7F00FF", "#FF007f", step))
    return [rgb_to_hex(v) for v in reversed(rainbow)]


def force_aspect(inner, outer, ratio):
    def force_ratio(event):
        w, h = event.width, int(event.width / ratio)
        if h > event.height:
            h = event.height
            w = int(event.height * ratio)
        inner.place(
            in_=outer,
            relx=0.5,
            rely=0.5,
            x=-0.5 * float(w),
            y=-0.5 * float(h),
            width=w,
            height=h,
        )

    outer.bind("<Configure>", force_ratio)


daymap = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

# T is datetime object
def get_day_of_week(t):
    return daymap.get(t.weekday())


def run_cl(commands: list):
    subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def open_link(link: str):
    print(f"Opening {link} in default web browser")
    webbrowser.open_new_tab(link)


def check_module_installed_status(module_name):
    reqs = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    installed_packages = [r.decode().split("==")[0] for r in reqs.split()]
    return module_name in installed_packages


def get_local_appdata_folder():
    return os.path.expandvars("%LOCALAPPDATA%")


def open_folder_in_window(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def sorted_dict_by_key(source: dict, reverse: bool = False):
    item = reversed(d.items()) if reverse else d.items()
    return OrderedDict(sorted(items, key=lambda k: k[0]))


class SuperWidgetMixin:
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
        self.bind("<Enter>", self._on_mouse_enter)
        self.bind("<Leave>", self._on_mouse_leave)
        self.bind("<Motion>", self._on_mouse_move)
        self.bind("<Button-1>", self._on_left_click)
        self.bind("<Button-2>", self._on_middle_click)
        self.bind("<Button-3>", self._on_right_click)
        self.bind("<Configure>", self._on_configure)
        self.bind("<MouseWheel>", self._on_mouse_wheel)

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


class PyScriptRunner:
    def __init__(self, script_path, print_function=print, cwd=os.getcwd()):
        self.script_path = script_path
        self.print_function = print_function
        self.cwd = cwd
        self.running = False

    def run(self, arguments):
        self.running = True
        wd = os.getcwd()
        os.chdir(self.cwd)
        args = [sys.executable, "-u", self.script_path]
        args.extend(arguments)
        try:
            p = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
            )
            with p.stdout:
                for line in iter(p.stdout.readline, b""):
                    self.do_print_function(line)
            p.wait()
        except Exception as e:
            self.do_print_function("ERROR - {e}")
        finally:
            os.chdir(wd)
            self.running = False

    def do_print_function(self, string):
        if self.print_function:
            self.print_function(string)
            sys.stdout.flush()
