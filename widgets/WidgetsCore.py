import tkinter as tk
from tkinter import ttk


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
