import platform
import tkinter as tk
from tkinter import ttk
from .WidgetsCore import SuperWidgetMixin
from .Scroller import Scroller, _create_container


class ScrolledListBox(Scroller, tk.Listbox, SuperWidgetMixin):
    @_create_container
    def __init__(self, master, widgetargs={}, **kw):
        tk.Listbox.__init__(
            self,
            master,
            **kw,
        )
        Scroller.__init__(self, master)
        SuperWidgetMixin.__init__(self, **widgetargs)


class Table(ttk.Frame):
    def __init__(self, *args, **kw):
        # self.on_selection_event = None
        # if "on_selection_event" in kw:
        #     self.on_selection_event = kw.pop("on_selection_event")
        ttk.Frame.__init__(self, *args, **kw)
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.config(command=self.on_scroll_bar)
        self.scrollbar.place(relx=1, relheight=1, width=20, x=-20)
        self.listbox_frame = ttk.Frame(self)
        self.listbox_frame.place(relheight=1, relwidth=1, width=-20)
        self.listboxes, self.categories, self.labels = {}, [], []

    def clear(self):
        for lb in self.listboxes:
            self.listboxes[lb].destroy()
        for l in self.labels:
            l.destroy()
        self.listboxes, self.categories, self.labels = {}, [], []

    def build(self, contents: dict):
        self.clear()
        self.categories = [k for k in contents.keys()]
        ratio = 1 / len(self.categories)
        i = 0
        for title in contents:
            l = ttk.Label(
                self.listbox_frame,
                text=title,
                style="Bold.TLabel",
            )
            l.place(relx=i * ratio, relwidth=ratio, height=20)
            self.labels.append(l)
            lb = self.listboxes[title] = tk.Listbox(
                self.listbox_frame,
                borderwidth=1,
                highlightthickness=0,
                exportselection=0,
                yscrollcommand=self.scrollbar.set,
            )
            lb.place(relx=i * ratio, relwidth=ratio, relheight=1, y=20, height=-20)
            lb.bind("<<ListboxSelect>>", self.on_selection)
            lb.bind("<ButtonPress-1>", self.on_press)
            for item in contents[title]:
                lb.insert("end", item)

            if platform.system() in ["Windows", "Darwin"]:
                lb.bind("<MouseWheel>", self.on_mouse_wheel)
            else:
                for k in ["<Button-4>", "<Button-5>"]:
                    lb.bind(k, self.on_mouse_wheel)
            i += 1

    def on_press(self, event):
        root = self.winfo_toplevel()
        cursor_y = root.winfo_pointery()
        l = event.widget
        cursor_y -= l.winfo_rooty()
        index = l.nearest(cursor_y)
        l.select_set(index)
        l.activate(index)
        for lb in self.listboxes:
            self.listboxes[lb].select_set(index)
            self.listboxes[lb].activate(index)
        # selection = lb.get(index)

    def on_mouse_wheel(self, event):
        l = self.listboxes[self.categories[0]]
        if platform.system() in ["Windows" or "Darwin"]:
            delta = event.delta
            if platform.system() == "Windows":
                delta = int(-1 * (event.delta / 120))
            l.yview("scroll", delta, "units")
        elif platform.system() == "Linux":
            if event.num == 5:
                l.yview("scroll", 1, "units")
            if event.num == 4:
                l.yview("scroll", -1, "units")
        for listbox in self.listboxes:
            self.listboxes[listbox].yview_moveto(l.yview()[0])
        return "break"

    def on_scroll_bar(self, move_type, move_units, __=None):
        if move_type == "moveto":
            for lb in self.listboxes:
                self.listboxes[lb].yview_moveto(move_units)

    def on_selection(self, event):
        l = event.widget
        index = l.curselection()
        l.select_set(index)
        l.activate(index)
        clicked_listbox = event.widget
        index = clicked_listbox.curselection()
        for lb in self.listboxes:
            self.listboxes[lb].selection_clear(0, tk.END)
            self.listboxes[lb].yview_moveto(clicked_listbox.yview()[0])
            self.listboxes[lb].select_set(index)
            self.listboxes[lb].activate(index)

        # if self.on_selection_event:
        #     self.on_selection_event(self.listboxes[self.categories[0]].get(index))

    def use_style(self, sty):
        self.tile_fill = sty.lookup("TEntry", "fieldbackground") or sty.lookup(
            "TCombobox", "fieldbackground"
        )
        bg = sty.lookup("TFrame", "background") or "#ffffff"
        fg = sty.lookup("TEntry", "foreground") or "#000000"
        for lb in self.listboxes:
            self.listboxes[lb].config(bg=bg)
            self.listboxes[lb].config(fg=fg)

    def get(self):
        lb = self.listboxes[self.categories[0]]
        return lb.get(lb.curselection())