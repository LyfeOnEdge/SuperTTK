import tkinter as tk
from tkinter import ttk

from ..widgets.WidgetsCore import default_pack
from ..widgets.ToplevelWidgets import FocusedToplevel, YesNoCancelWindow, NoticeWindow
from ..widgets.EntryWidgets import LabeledEntry
from ..widgets.ListBoxWidgets import Table
from ..utils.ProfilesSystem import UserProfile

class ProfilesWindow(FocusedToplevel):
    def __init__(self, app):
        FocusedToplevel.__init__(self, window=app.window)
        if not app.profiles_enabled:
            raise ValueError("Attempted to instantiate the profile manager window but user profiles are disabled.")
        self.app = app
        self.title="Profile Manager"
        self.listbox = Table(self.frame)
        self.refresh_profile_listbox()
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.update_idletasks()
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(side=tk.BOTTOM, fill="x", expand=True, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(
            side=tk.LEFT, fill="x", expand=True
        )
        ttk.Button(button_frame, text="Delete Profile", command=self.on_delete).pack(
            side=tk.LEFT, fill="x", expand=True
        )
        ttk.Button(button_frame, text="Edit Profile", command=self.on_edit).pack(
            side=tk.LEFT, fill="x", expand=True
        )
        self._finish_setup()

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
            EditorWindow(self.app, prof)
        else:
            raise ValueError("Invalid profile to edit")

    def _on_cancel(self, event=None):
        self.destroy()

class EditorWindow(FocusedToplevel):
    def __init__(self, app, profile):
        self.app, self.profile = app, profile
        FocusedToplevel.__init__(self, window=app.window)
        self.username_box = LabeledEntry(self.frame, labeltext="Username")
        self.username_box.set(profile.username)
        self.username_box.pack(side=tk.TOP, expand=False, fill="x")
        ttk.Label(self.frame, text="User Values", font=self.app.bold_font, justify=tk.CENTER, anchor=tk.CENTER).pack(side=tk.TOP, fill="x", expand=False)
        self.table = Table(self.frame)
        data = profile.data["preferences"]
        data = {
            "Key":list(data.keys()),
            "Value":[data[k] for k in data],
        }
        self.table.build(data)
        self.table.pack(side=tk.TOP, fill="x")

        ttk.Button(self.frame, text="Add New Key", command=self._on_save).pack(
            side=tk.TOP, expand=False, fill="x"
        )
        ttk.Button(self.frame, text="Edit Selected Key", command=self._on_save).pack(
            side=tk.TOP, expand=False, fill="x"
        )
        ttk.Button(self.frame, text="Delete Selected Key", command=self._on_save).pack(
            side=tk.TOP, expand=False, fill="x"
        )

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(side=tk.TOP, fill="x", expand=True, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(
            side=tk.LEFT, expand=True, fill="x"
        )
        ttk.Button(button_frame, text="Save", command=self._on_save).pack(
            side=tk.LEFT, expand=True, fill="x"
        )
        self.title(f"Editing Profile - {profile.username}")
        self.update_idletasks()
        minsize = 200
        width = self.winfo_width() if self.winfo_width() > minsize else minsize
        height = self.winfo_height() if self.winfo_height() > minsize else minsize 
        self.geometry(f"{width}x{height}")
        self._finish_setup()

    def cancel(self, event=None):
        self.destroy()

    def save(self, event=None):
        profile.save()

    def _on_cancel(self, event=None):
        pass


    def _on_save(self, event=None):
        pass


