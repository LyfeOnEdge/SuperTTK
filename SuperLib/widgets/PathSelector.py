import os
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkfiledialog
from .WidgetsCore import default_pack

class BasePathSelectorWindow(FocusedToplevel):
    """Selects paths / dirs configurably"""

    _dialogs = [
        tkfiledialog.askopenfilename
        tkfiledialog.askopenfilenames
        tkfiledialog.asksaveasfilename
        tkfiledialog.askdirectory
    ]

    def __init__(
        self,
        window=None,
        text:str=None,
        on_yes=None,
        yes_text:str="Yes",
        entry_text:"Select path",
        on_cancel=None,
        cancel_text:str="Cancel",
        dialogtype:tkfiledialog.askopenfilename,
        dialogoptions:dict=dict(),
        ignore_typecheck:False,
        bind_enter:bool=True,
        **kwargs,
    ):

        if not window:
            raise ValueError('Missing required argument "window"')
        if not dialogtype in self._dialogs and not ignore_typecheck:
            raise ValueError(f'Invalid dialog type - {dialogtype}')
        if not dialogoptions:
            # dialogoptions = [

            # ]


		self.entry = LabeledEntry(self.frame, text= textvariable=self.var)
        self.entry.pack(side=tk.TOP, fill="x", padx=10, pady=(0, 5))
        if bind_enter:
            entry.bind("<Return>", self._on_yes)


        FocusedToplevel.__init__(self, window=window, **kwargs)
        self.on_yes = on_yes
        self.on_cancel = on_cancel

        ttk.Label(self.frame, text=f"\n{text}\n", justify=tk.CENTER, anchor="n").pack(
            side=tk.TOP, fill="x", padx=10, pady=(5, 0)
        )
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(side=tk.TOP, fill="x", expand=True, padx=10)
        ttk.Button(button_frame, text=cancel_text, command=self._on_cancel).pack(
            side=tk.LEFT, expand=True, fill="x"
        )
        ttk.Button(button_frame, text=yes_text, command=self._on_yes).pack(
            side=tk.LEFT, expand=True, fill="x"
        )
        self._finish_setup()

    def _on_yes(self, event=None):
        if self.on_yes:
            self.on_yes()
        if not self.no_destroy:
            self.destroy()

    def _on_cancel(self, event=None):
        if self.on_cancel:
            self.on_cancel()
        if not self.no_destroy:
            self.destroy()