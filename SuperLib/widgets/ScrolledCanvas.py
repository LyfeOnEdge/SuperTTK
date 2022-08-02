import platform
import tkinter as tk
from tkinter import ttk
from .ResizableCanvas import ResizableCanvas
from .Scroller import _on_mousewheel

class ScrolledCanvas(ttk.Frame):
    """Resizeable, Auto-Scrollbarred Canvas"""

    __desc__ = "Canvas resizes to fit frame on configure event. Canvas has automatic Scrollbars that appear when needed. Canvas background color is based on current theme. Due to how the scrolling is handled the actual Canvas is accessd via `ScrolledCanvas().canvas`."
    def __init__(
        self,
        parent,
        on_mouse_enter=None,  # If specified, calls func(event)
        on_mouse_leave=None,  # If specified, calls func(event)
        on_mouse_move=None,  # If specified, calls func(event)
        on_mouse_wheel=None,  # If specified, calls func(event)
        on_left_click=None,  # If specified, calls func(event)
        on_middle_click=None,  # If specified, calls func(event)
        on_right_click=None,  # If specified, calls func(event)
        on_configure=None,  # If specified, calls func(event)
        bind_canvas_scroll=True,
        **kw,  # Canvas args
    ):
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_leave = on_mouse_leave
        self.on_mouse_move = on_mouse_move
        self.on_left_click = on_left_click
        self.on_middle_click = on_middle_click
        self.on_right_click = on_right_click
        self.on_mouse_wheel = on_mouse_wheel
        self.on_configure = on_configure
        ttk.Frame.__init__(self, parent)
        self.canvas_height = 1
        self.canvas_width = 1
        self.canvas = ResizableCanvas(self, **kw)
        self.canvas.config(
            width=self.canvas_width, height=self.canvas_height, highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.config(command=self._on_scroll_bar)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.canvas_frame = ttk.Frame(self.canvas)
        self.canvas_frame.config(width=self.canvas_width, height=self.canvas_height)
        self.canvas.create_window(0, 0, window=self.canvas_frame, anchor="nw")
        self.canvas.config(scrollregion=(0, 0, self.canvas_height, self.canvas_height))
        self.canvas.bind("<Enter>", self._on_mouse_enter, add="+")
        self.canvas.bind("<Leave>", self._on_mouse_leave, add="+")
        self.canvas.bind("<Motion>", self._on_mouse_move, add="+")
        self.canvas.bind("<Button-1>", self._on_left_click, add="+")
        self.canvas.bind("<Button-2>", self._on_middle_click, add="+")
        self.canvas.bind("<Button-3>", self._on_right_click, add="+")
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel, add="+")
        self.canvas.bind("<Configure>", self._on_configure, add="+")
        self.bind_canvas_scroll = bind_canvas_scroll

    def get_adjusted_y_view(self, event):
        """Gets a canvas y-view adjusted based on its scrolled position"""
        return int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))

    def _on_mouse_enter(self, event):
        if self.on_mouse_enter:
            self.on_mouse_enter(event, (event.x, self.get_adjusted_y_view(event)))

    def _on_mouse_leave(self, event):
        if self.on_mouse_leave:
            self.on_mouse_leave(event, (event.x, self.get_adjusted_y_view(event)))

    def _on_mouse_move(self, event):
        x, y = event.x, self.get_adjusted_y_view(event)
        if self.on_mouse_move:
            self.on_mouse_move(event, (event.x, self.get_adjusted_y_view(event)))

    def _on_scroll_bar(self, move_type:str, move_units:float, __=None):
        if move_type == "moveto":
            self.canvas.yview("moveto", move_units)

    def _on_mouse_wheel(self, event):
        if self.on_mouse_wheel:
            self.on_mouse_wheel(event)
        if self.bind_canvas_scroll:
            _on_mousewheel(event, self.canvas)

    def _on_left_click(self, event):
        y = self.get_adjusted_y_view(event)
        x = event.x
        if self.on_left_click:
            self.on_left_click(event, (x, y))

    def _on_middle_click(self, event):
        if self.on_middle_click:
            self.on_middle_click(event, (event.x, self.get_adjusted_y_view(event)))

    def _on_right_click(self, event):
        if self.on_right_click:
            self.on_right_click(event, (event.x, self.get_adjusted_y_view(event)))

    def _on_configure(self, event=None):
        if hasattr(self, "refresh"):
            self.refresh()
        w, h = self.winfo_width(), self.winfo_height()
        self.canvas.config(width=w, height=h)
        if self.on_configure:
            self.on_configure(w, h)

    def use_style(self, style):
        """Reformat with a given ttk style. `Returns None`"""
        if self.winfo_exists():
            self.tile_fill = style.lookup("TEntry", "fieldbackground") or style.lookup(
                "TCombobox", "fieldbackground"
            )
            bg = style.lookup("TFrame", "background") or "#ffffff"
            self.canvas.configure(bg=bg)
            if hasattr(self, "refresh"):
                self.refresh()


class TiledCanvas(ScrolledCanvas):
    def __init__(
        self,
        *args,
        tile_width=400,
        tile_height=100,
        tile_padx=5,
        tile_pady=5,
        tile_color="#424548",
        text_color="#CCCCCC",
        border_color="#000000",
        on_tile_left_click=None,
        on_tile_middle_click=None,
        on_tile_right_click=None,
        override_tile_width=False,
        **kw,
    ):
        ScrolledCanvas.__init__(self, *args, **kw)
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_padx = tile_padx
        self.tile_pady = tile_pady
        self.tiles = []
        self.tile_color = tile_color
        self.text_color = text_color
        self.border_color = border_color
        self.on_tile_left_click = on_tile_left_click
        self.on_tile_middle_click = on_tile_middle_click
        self.on_tile_right_click = on_tile_right_click
        self.override_tile_width = override_tile_width
        self.hovered = None
        self.canvas.bind("<Motion>", self.__on_mouse_move)
        self.canvas.bind("<Button-1>", self.__on_left_click)
        self.canvas.bind("<Button-2>", self.__on_middle_click)
        self.canvas.bind("<Button-3>", self.__on_right_click)

    def refresh(self, event=None):
        """Redraw the canvas"""
        self.canvas.delete("all")
        i = 0
        framewidth = self.canvas.winfo_width() - self.tile_padx
        self.canvas_frame.config(width=framewidth)
        # Get number of tiles fittable in the window
        maxperrow = framewidth // (self.tile_width + self.tile_padx)
        # If there's not enough room to build anything
        if not maxperrow:
            if self.override_tile_width:
                maxperrow = 1
            else:
                return  # print("Not_enough_room")
        maxwidth = (maxperrow) * self.tile_width + maxperrow * self.tile_padx
        filler_space = framewidth - maxwidth
        try:
            filler_space = filler_space / (maxperrow + 1)
        except ZeroDivisionError:
            return
        _x = 0
        _y = 0
        for t in self.tiles:
            __x = (
                _x * self.tile_width
                + (_x + 1) * self.tile_padx
                + (_x + 1) * filler_space
            )
            __y = _y * self.tile_height + (_y + 1) * self.tile_pady
            t.set_position(__x, __y)
            self._place_tile(t)
            # handle_tile(t, place_x, place_y)
            i += 1
            _x += 1
            if _x == maxperrow:
                _x = 0
                _y += 1
        _y += 1
        height = _y * self.tile_height + (_y + 1) * self.tile_pady
        frameheight = self.canvas_frame.winfo_height()
        height = height if height > frameheight else frameheight
        self.canvas_height = height
        self.canvas_frame.config(height=self.winfo_height())
        self.canvas.config(scrollregion=(0, 0, 0, self.canvas_height))

    def _place_tile(self, tile):
        tile.references.extend(
            [
                self.canvas.create_rectangle(
                    tile.x,
                    tile.y,
                    tile.x + self.tile_width,
                    tile.y + self.tile_height,
                    fill=self.tile_fill,
                ),
                self.canvas.create_text(
                    tile.x + 5, tile.y + 10, anchor="nw", text=tile.text
                ),
            ]
        )
        if tile.active:
            self._activate_tile(tile)

    def _activate_tile(self, tile):
        tile.active_references.extend(
            [
                self.canvas.create_rectangle(
                    tile.x,
                    tile.y,
                    tile.x + self.tile_width,
                    tile.y + self.tile_height,
                    outline=self.border_color,
                    width=4,
                ),
                self.canvas.create_rectangle(
                    tile.x + 4,
                    tile.y + 4,
                    tile.x + self.tile_width - 5,
                    tile.y + self.tile_height - 5,
                    fill=self.tile_color,
                ),
                self.canvas.create_text(
                    tile.x + 8,
                    tile.y + 8,
                    text=f"Hovered {tile.text}",
                    anchor="nw",
                    width=self.tile_width - 16,
                    fill=self.text_color,
                ),
            ]
        )

    def _deactivate_tile(self, tile):
        for r in tile.active_references:
            self.canvas.delete(r)

    def _on_action(self, event, on_find_action=None):
        x, y = event.x, self.get_adjusted_y_view(event)
        found = False
        for t in self.tiles:
            if not found:
                if t.is_in_range(x, y):
                    found = True
                    self.hovered = t
                    t.activate()
                    if on_find_action:
                        on_find_action(t)
                else:
                    t.deactivate()
            else:
                t.deactivate()
        if not found:
            self.hovered = None

    def __on_mouse_move(self, event):
        self._on_mouse_move(event)
        self._on_action(event)

    def __on_left_click(self, event):
        self._on_left_click(event)

        def on_left_click(tile):
            if self.on_tile_left_click:
                self.on_tile_left_click(tile)

        self._on_action(event, on_find_action=on_left_click)

    def __on_middle_click(self, event):
        self._on_middle_click(event)

        def on_middle_click(tile):
            if self.on_tile_middle_click:
                self.on_tile_middle_click(tile)

        self._on_action(event, on_find_action=on_middle_click)

    def __on_right_click(self, event):
        self._on_right_click(event)

        def on_right_click(tile):
            if self.on_tile_right_click:
                self.on_tile_right_click(tile)

        self._on_action(event, on_find_action=on_right_click)


class ExampleTile:
    """An example tile for a Scrolled Canvas"""
    def __init__(self, manager, text):
        self.x, self.y = 0, 0
        self.manager = manager
        self.text = text
        self.thumbnail = None
        self.references = []
        self.active_references = []
        self.active = False

    def set_position(self, x, y):
        """Sets a tiles position for the draw manager's draw method."""
        self.x, self.y = x, y

    def activate(self):
        """Calls the manager to activate the widget."""
        if not self.active:
            self.active = True
            self.manager._activate_tile(self)

    def deactivate(self):
        """Calls the manager to deactivate the widget."""
        if self.active:
            self.active = False
            self.manager._deactivate_tile(self)

    def is_in_range(self, pointer_x, pointer_y):
        """Checks if the mouse pointer is in the tile."""
        x, y = pointer_x, pointer_y
        lb = self.x
        rb = lb + self.manager.tile_width
        tb = self.y
        bb = tb + self.manager.tile_height
        return all((x > lb, x < rb, y > tb, y < bb))
