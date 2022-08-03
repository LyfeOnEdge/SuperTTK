from tkinter import ttk


class EasySizegrip(ttk.Sizegrip):
    """Sizegrip widget with bindings"""

    __desc__ = "Automatically packs self and binds mouse presses for systems that don't bind automatically."
    def __init__(self, *args, **kwargs):
        ttk.Sizegrip.__init__(self, *args, **kwargs)
        self.place(relx=1.0, rely=1.0, anchor="se")
        self.bind("<ButtonPress-1>", self._on_grip_press, add="+")
        self.bind("<B1-Motion>", self._on_grip_move, add="+")
        self.bind("<ButtonRelease-1>", self._on_grip_release, add="+")

    def _on_grip_release(self, event):
        """Optionally redefine this in subclass"""

    def _on_grip_move(self, event):
        """Optionally redefine this in subclass"""

    def _on_grip_press(self, event):
        self["cursor"] = "bottom_right_corner"
