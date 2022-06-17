from tkinter import ttk


class EasySizegrip(ttk.Sizegrip):
    def __init__(self, *args, **kwargs):
        ttk.Sizegrip.__init__(self, *args, **kwargs)
        self.place(relx=1.0, rely=1.0, anchor="se")
        self.bind("<ButtonPress-1>", self._on_grip_press)
        self.bind("<B1-Motion>", self._on_grip_move)
        self.bind("<ButtonRelease-1>", self._on_grip_release)

    def _on_grip_release(self, event):
        """Optionally redefine this in subclass"""
        return

    def _on_grip_move(self, event):
        """Optionally redefine this in subclass"""
        return

    def _on_grip_press(self, event):
        self["cursor"] = "bottom_right_corner"
