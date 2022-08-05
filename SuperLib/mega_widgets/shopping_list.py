import tkinter as tk
from tkinter import ttk
from ..widgets.Tabs import Tab
from ..widgets.EntryWidgets import LabeledButtonEntry
from ..widgets.ComboboxWidgets import LabeledCombobox
from ..widgets.TextWidgets import CopyBox
from ..widgets.WidgetsCore import default_pack
from ..widgets.ListBoxWidgets import Table
from ..utils.HTML_Generator import HTML_Generator

MODULE_PREFIX="Shopping."

class ShoppingListTab(Tab):
    def __init__(self, notebook:ttk.Notebook, app):
        Tab.__init__(self, notebook, "Shopping List")
        ShoppingList(self, app).pack(fill=tk.BOTH, expand=True)

class ShoppingList(ttk.Frame):
    def __init__(self, parent, app):
        ttk.Frame.__init__(self, parent)
        self.app = app
        self.source_favorites_list = []
        self.favorites_list = []
        self.shopping_list = []

        if self.app.profiles_enabled:
            prof = self.app.profiles.current_profile
            self.source_favorites_list = prof.get_preference(MODULE_PREFIX+"favorites") or []
            self.shopping_list = prof.get_preference(MODULE_PREFIX+"cart") or []

        self.update_favorites()

        lists_frame = ttk.Frame(self)
        lists_frame.pack(fill=tk.BOTH, expand=True, padx=10)
    
        fav_col = ttk.Frame(lists_frame)
        fav_col.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
##        default_pack(ttk.Label(fav_col, text="Favorites",anchor=tk.CENTER, style="Bold.TLabel"))
        
        self.favorites_table = Table(fav_col, visible_rows=1)
        self.favorites_table.pack(fill=tk.BOTH, expand=True)
        self.favorites_box = LabeledButtonEntry(fav_col, labeltext="New fav ", button_text=">", is_child=True, command=self.add_to_favorites_list)
        self.favorites_box.button.configure(width=0)
        self.favorites_box.button.pack(padx=0, pady=0, expand=False, fill="y", ipadx=0)
        default_pack(self.favorites_box)
        add_button = ttk.Button(fav_col, text="Add fav to cart", command=self.add_fav_to_shopping_list)
        default_pack(add_button)
        rem_button = ttk.Button(fav_col, text="Forget favorite", command=self.forget_favorite)
        default_pack(rem_button)

        sel_col = ttk.Frame(lists_frame)
        sel_col.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
##        default_pack(ttk.Label(sel_col, text="Shopping List",anchor=tk.CENTER, style="Bold.TLabel"))
        
        self.shopping_table = Table(sel_col, visible_rows=1)
        self.shopping_table.pack(fill=tk.BOTH, expand=True)
        self.shopping_box = LabeledButtonEntry(sel_col, labeltext="Add item ", button_text=">", is_child=True, command=self.add_to_shopping_list)
        self.shopping_box.button.configure(width=0)
        self.shopping_box.button.pack(padx=0, pady=0, expand=False, fill="y", ipadx=0)
        default_pack(self.shopping_box)
        del_button = ttk.Button(sel_col, text="Remove from cart", command=self.remove_item_from_shopping_list)
        default_pack(del_button)
        clr_button = ttk.Button(sel_col, text="Clear cart list", command=self.clear_shopping_list)
        default_pack(clr_button)

        export_button = ttk.Button(self, text="Export Shopping List", command=self.export_html)        
        export_button.pack(side=tk.BOTTOM, pady=10, padx=10, fill="x")
        self.update()
        
    def update(self):
        self.update_favorites()
        self.favorites_table.clear()
        self.favorites_table.build({"Favorites":self.favorites_list})
        self.favorites_table.use_style(self.app.style)
        self.shopping_table.clear()
        self.shopping_table.build({"Shopping Cart":self.shopping_list})
        self.shopping_table.use_style(self.app.style)
        if self.app.profiles_enabled:
            prof = self.app.profiles.current_profile
            prof.data["preferences"][MODULE_PREFIX+"favorites"]=self.source_favorites_list
            prof.data["preferences"][MODULE_PREFIX+"cart"]=self.shopping_list
            prof.save()
            
    def update_favorites(self):
        self.favorites_list.clear()
        self.source_favorites_list = sorted(self.source_favorites_list)
        for item in self.source_favorites_list:
            if not item in self.shopping_list:
                self.favorites_list.append(item)

    def add_to_shopping_list(self, item):
        if item:
            item=item.strip()
            self.shopping_list.append(item)
        self.shopping_box.clear()
        self.update()

    def add_fav_to_shopping_list(self):
        fav = self.favorites_table.get()
        if fav:
            fav=fav[0].strip()
            self.add_to_shopping_list(fav)
        self.update()

    def remove_item_from_shopping_list(self):
        item = self.shopping_table.get()
        if item:
            self.shopping_list.remove(item[0])
        self.update()
        
    def add_to_favorites_list(self, item:str):
        item=item.strip()
        if item and not item in self.source_favorites_list:
            self.source_favorites_list.append(item)
        self.favorites_box.clear()
        self.update()

    def clear_shopping_list(self):
        self.shopping_list.clear()
        self.update()

    def forget_favorite(self):
        fav = self.favorites_table.get()
        if fav:
            fav=fav[0].strip()
            self.source_favorites_list.remove(fav)
        self.update()
        
    def export_html(self):
        print("Exporting Shopping List")
        generator = HTML_Generator()
        r = len(self.shopping_list)
        for i in range(r):
            generator.start_div()
            generator.add_center('<input type="checkbox" class="larger">')
            generator.add_center(f'<h1>{str(self.shopping_list[i])}</h1>')
            if i < r-1:
                generator.end_div()
                generator.add_divider()
        print(generator.assemble())
        import tempfile
        file = tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".html")
        generator.save(file.name)
        import webbrowser
        webbrowser.open(file.name)