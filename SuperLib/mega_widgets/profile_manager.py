import tkinter as tk
from tkinter import ttk
from copy import deepcopy
from ..widgets.WidgetsCore import default_pack
from ..widgets.ToplevelWidgets import FocusedToplevel, YesNoCancelWindow, NoticeWindow, PromptWindow
from ..widgets.EntryWidgets import LabeledEntry
from ..widgets.ListBoxWidgets import Table
from ..widgets.RadiobuttonWidgets import LabeledRadiobutton
from ..utils.ProfilesSystem import UserProfile
from ..utils.utils import get_friendly_time

class ProfilesWindow(FocusedToplevel):
    def __init__(self, app):
        FocusedToplevel.__init__(self, window=app.window, on_close=self._on_cancel)
        if not app.profiles_enabled:
            raise ValueError("Attempted to instantiate the profile manager window but user profiles are disabled.")
        self.app = app
        self.title("Profile Manager")
        self.listbox = Table(self.frame)
        self.refresh_profile_listbox()
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(10,0))
        self.update_idletasks()
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(side=tk.BOTTOM, fill="x", expand=False, padx=10, pady=(0,10))
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(
            side=tk.LEFT, fill="x", expand=True
        )
        ttk.Button(button_frame, text="Delete Profile", command=self.on_delete).pack(
            side=tk.LEFT, fill="x", expand=True
        )
        ttk.Button(button_frame, text="Edit Profile", command=self.on_edit).pack(
            side=tk.LEFT, fill="x", expand=True
        )
        minsize = 400
        width = self.winfo_width() if self.winfo_width() > minsize else minsize
        height = self.winfo_height() if self.winfo_height() > minsize else minsize 
        self.geometry(f"{width}x{height}")
        self._finish_setup()
        self.update_idletasks()

    def refresh_profile_listbox(self):
        self.listbox.clear()
        self.listbox.build({"Profiles":self.app.profiles.get_profile_names()})

    def on_delete(self, event=None):
        value = self.listbox.get()
        if not value:
            NoticeWindow(window=self, text=f'Please select an option from the profiles list.')
            return
        prof = self.app.profiles.get_profile_by_username(value[0])
        if prof:
            if prof == self.app.profiles.current_profile:
                NoticeWindow(window=self, text=f'Cannot delete selected profile\n"{prof.username}"\nProfile is currently in use.\nUse a different profile to delete this one')
                return
            YesNoCancelWindow(window = self, text=f"Are you sure you want to delete profile - {prof.username}?", on_yes=lambda:self._on_delete(prof), yes_text="Delete", no_enabled=False)
        else:
            raise ValueError("Invalid profile to delete")

    def _on_delete(self, profile:UserProfile):
        print(f"Deleting profile with username {profile.username}.")
        self.app.profiles.delete_profile(profile)
        self.refresh_profile_listbox()
    
    def on_edit(self, event=None):
        value = self.listbox.get()
        if not value:
            NoticeWindow(window=self, text=f'Please select an option from the profiles list.')
            return
        prof = self.app.profiles.get_profile_by_username(value[0])
        if prof:
            f = EditorFrame(self, self.app, prof)
            self.update_idletasks()
            minsize = 400
            width = f.winfo_reqwidth() if f.winfo_reqwidth() > minsize else minsize
            height = f.winfo_reqheight() if f.winfo_reqheight() > minsize else minsize
            self.resizable(True,True)
            self.geometry(f"{width}x{height}")
            self.resizable(False,False)
        else:
            raise ValueError("Invalid profile to edit")

    def _on_cancel(self, event=None):
        self.destroy()
        self.update_idletasks()
        self.app._select_profile(self.app.profiles.current_profile)

class EditorFrame(ttk.Frame):
    def __init__(self, parent, app, profile):
        self.app, self.parent, self.profile = app, parent, profile
        ttk.Frame.__init__(self, parent)
        self.place(relwidth=1, relheight=1)
        self.tempdata = deepcopy(self.profile.data)
        values_frame = ttk.LabelFrame(self, text="User Values")
        values_frame.pack(fill="x", padx=10,pady=(0,10))
        self.username_box = LabeledEntry(values_frame, labeltext="Username")
        self.username_box.set(profile.username)
        self.username_box.pack(side=tk.TOP, expand=False, fill="x")
        atomic_box = LabeledEntry(values_frame, labeltext="Atomic")
        atomic_box.set(self.tempdata["atomic"]) 
        atomic_box.pack(side=tk.TOP, expand=False, fill="x")
        atomic_box.disable()
        edited_box = LabeledEntry(values_frame, labeltext="Last Settings Change")
        edited_box.set(self.tempdata["last_edited"])
        edited_box.pack(side=tk.TOP, expand=False, fill="x")
        edited_box.disable()
        edited_box = LabeledEntry(values_frame, labeltext="Last Accessed")
        edited_box.set(self.tempdata["last_accessed"])
        edited_box.pack(side=tk.TOP, expand=False, fill="x")
        edited_box.disable()
        prefs_frame = ttk.LabelFrame(self, text="User Preferences")
        prefs_frame.pack(fill="both", padx=10,pady=(0,10),expand=True)
        self.table = Table(prefs_frame, visible_rows=6)
        self.rebuild_table()
        self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        ttk.Button(prefs_frame, text="Add New Key", command=self.on_add).pack(side=tk.TOP, expand=False, fill="x")
        ttk.Button(prefs_frame, text="Edit Selected Key", command=self.on_edit).pack(side=tk.TOP, expand=False, fill="x")
        ttk.Button(prefs_frame, text="Delete Selected Key", command=self.on_delete).pack(side=tk.TOP, expand=False, fill="x")
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill="x", expand=False, padx=10, pady=(0,10))
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side=tk.LEFT, fill="x", expand=True)
        ttk.Button(button_frame, text="Save Changes", command=self.on_save).pack(side=tk.LEFT, fill="x", expand=True)

    def on_add(self):
        """Get new key name from user"""
        PromptWindow(window=self.parent, text=f'Enter name for new key', on_yes=self._on_add)

    def _on_add(self, key):
        """Get new key value from user"""
        self.update_idletasks()
        PromptWindow(window=self.parent, text=f'Enter value for new key - {key}', on_yes=self.get_add_handler(key), select_type=True)._finish_setup()

    def get_add_handler(self, key):
        def handler(val):
            self.tempdata["preferences"][key]=val
            self.rebuild_table()
        return handler

    def on_edit(self):
        vals = self.table.get()
        if not vals:
            return NoticeWindow(window=self.parent, text=f'Please select a key to edit.')
        win = PromptWindow(window=self.parent, text=f'Enter new value for key "{vals[0]}"', on_yes=self.get_edit_handler(vals[0]), select_type=True)
        win.var.set(vals[1])

    def get_edit_handler(self, key:str):
        def handler(val):
            self.tempdata["preferences"][key]=val
            self.rebuild_table()
        return handler

    def on_delete(self):
        vals = self.table.get()
        if not vals:
            return NoticeWindow(window=self.parent, text=f'Please select a key to delete.')
        YesNoCancelWindow(window=self.parent, text=f'Are you sure you want to delete user preferences key "{vals[0]}"?', on_yes=self.get_delete_handler(vals[0]), no_enabled=False)
        
    def get_delete_handler(self, key:str):
        def handler():
            self.tempdata["preferences"].pop(key)
            self.rebuild_table()
        return handler

    def on_save(self, event=None):
        print(f"Saving changes to {self.profile.username}")
        self.profile.data=self.tempdata
        self.destroy()

    def on_cancel(self):
        if not self.tempdata == self.profile.data:
            YesNoCancelWindow(window=self.parent, text="You have unsaved changes, would you like to save?", on_yes=self.on_save, on_no=self.destroy)
        else:
            self.destroy()

    def rebuild_table(self):
        self.table.clear()
        prefs = self.tempdata["preferences"]
        prefs = {
            "Key":list(prefs.keys()),
            "Value":[prefs[k] for k in prefs],
        }
        self.table.build(prefs)
