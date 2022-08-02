#!/usr/bin/env python3
#
# explorer_tk
# Copyright (C) 2020 Andrew Spangler
#
desc = """
explorer.py
A simple file explorer and file/folder picker widget written in tkinter/python.
"""
module_usage = """
The explorer, file, and folder pickers are accessed through three objects;
explorer, file_dialog, and folder_dialog respectively.

The explorer offers nothing more than simple browsing, no input can be obtained. 

Input from file_dialog and folder_dialog windows is obtained like this:
    ```
    dialog = file_dialog()
    file_path = dialog.get_input()
    ```
"""
import io, os, sys, argparse, platform, threading
from datetime import datetime
import tkinter as tk
from tkinter.ttk import (
    Notebook,
    Style,
    Label,
    Frame,
    Button,
    LabelFrame,
    Entry,
    Progressbar,
    Treeview,
)
from PIL import Image, ImageTk

from .TreeviewWidgets import ScrolledTree

WIDTH = 550
HEIGHT = 400

file_image_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x01\x85iCCPICC Profile\x00\x00x\x9c}\x91=H\xc3P\x14\x85OS\xb5"\x15\x05;\x888d\xa8N\x16D\x8b8J\x15\x8b`\xa1\xb4\x15Zu0y\xe9\x1f4iHR\\\x1c\x05\xd7\x82\x83?\x8bU\x07\x17g]\x1d\\\x05A\xf0\x07\xc4\xc9\xd1I\xd1EJ\xbc/)\xb4\x88\xf1\xc1\xe5}\x9c\xf7\xce\xe1\xbe\xfb\x00\xa1Qa\xaa\xd95\t\xa8\x9ae\xa4\xe211\x9b[\x15\x03\xaf\xe8\xc1 U\x0f\xa2\x123\xf5Dz1\x03\xcf\xf5u\x0f\x1f\xdf\xef"<\xcb\xfb\xde\x9f\xab_\xc9\x9b\x0c\xf0\x89\xc4sL7,\xe2\r\xe2\x99MK\xe7\xbcO\x1cb%I!>\'\x9e0\xa8A\xe2G\xae\xcb.\xbfq.:,\xf0\xcc\x90\x91I\xcd\x13\x87\x88\xc5b\x07\xcb\x1d\xccJ\x86J\x1c%\x0e+\xaaF\xf9B\xd6e\x85\xf3\x16g\xb5Rc\xad>\xf9\x0b\x83ym%\xcdu\xaaQ\xc4\xb1\x84\x04\x92\x10!\xa3\x862*\xb0\x10\xa1]#\xc5D\x8a\xcec\x1e\xfe\x11\xc7\x9f$\x97L\xae2\x189\x16P\x85\n\xc9\xf1\x83\xff\xc1\xef\xd9\x9a\x85\xe9)7)\x18\x03\xba_l\xfbc\x0c\x08\xec\x02\xcd\xbam\x7f\x1f\xdbv\xf3\x04\xf0?\x03WZ\xdb_m\x00\xb3\x9f\xa4\xd7\xdbZ\xf8\x08\x18\xd8\x06.\xae\xdb\x9a\xbc\x07\\\xee\x00\xc3O\xbadH\x8e\xe4\xa7\x12\n\x05\xe0\xfd\x8c\xbe)\x07\x0c\xdd\x02}k\xee\xdcZ\xe78}\x0024\xab\xe5\x1b\xe0\xe0\x10\x18/R\xf6\xba\xc7\xbb{;\xe7\xf6\xef\x9d\xd6\xfc~\x00`\xe2r\xa0\t\x11xT\x00\x00\x00\xaeIDATx\x9c\xed\xd3\xb1m\x02A\x10\x85\xe1\xcf`\x049\xc4n\x81\x80\x90\x06h\x80\x147@D9T\xe1\xc0\x0e!\xa2\x02\x02\xb2+\x00\x89\x88\xf4\xf0A\xb0\xcbi\x85\x04,\x90\xf2K\xa3\x1di\xf4\x9e\xdeH\xb3\x04\xbeP\xe0x\xa7~\xd0\x91\xf0\x19\xdf\x01v\x98\xb8\xce\x083\xcc1\xc5>\x1d\x8e\xf1wC\x0c\xdf\xd8`\x8b\x05\xba\xd0\x88\xc3c\xd2_\xa3\xc0\x1aK\xf41LW\xc8a\x15\x0b~\xd1N\x13<JSH\xfd\xb4A\xcd\xdb \xcf\xa0\xf5\xaaA\x99c\xf0\x81*\xc3\xecL\x155\xf5%\x1e\xd0\x13\xce\xb3\x14\x0e\xe52]\x85\x7fa\xa5^\xd4\xd4\xe4~\xe7s\x15Q\xe3\x04\xf1\x8b-U0%pD\x00\x00\x00\x00IEND\xaeB`\x82'
folder_image_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\xc6IDATx\x9c\xcd\xd3?J\x03A\x14\xc7\xf1\xcf\xae\x81\x80M\"\xe8\r<\xc2\n\xe9C\x12<\x89\xd7\xf0\x04)<\x82\xc7\xf0\x0c\x1e@\xd0\xce\xd2\x94i6\x90]\x8b\xbc\x818\xc9\xe2&6\xfe`\x8a\xf7\xe7\xf7\x9d\xf7\x18\x86?\xaa\xc0\x0cs\\d\xf9/<a\xfd\x1b\xa0\xc63>PF\xbe\r\xf0'\x96\x11\xe7\xbe-\xde\x8b(\xde\xe15k\xba\x0e\xf0U4\x17{\xb5\x16\x97X\xa5`\xd21a\x19\x80qvFX\xa0\x1dD\xe3c\xd0\xca\x9f~\xcd\x91\xf1S\xfe\x06\x12\xe0-V\xc8\x01]jP\xe1>\xadP\xf54\xee\xabB\x9bn\x1c\x9e\x01\x18\xd2\x7f\xe4N\xfd\x1f@}\x86\xb7f\xf7\x8c\x1b<`z\xc2D\rn\xb1\xe9\xfaL}\xb4\xc5\xcb\x89\x9eC}\x03\xeb\x12%\xc6_\xc2-\xa0\x00\x00\x00\x00IEND\xaeB`\x82"

##TODO:
# - Bar to display allowed file types
# - Icons for different file types
# - Bind enter to submit text response


class DirEntry:
    """Fake DirEntry object to emulate os.DirEntry"""

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.isfile = os.path.isfile(self.path)

    def is_dir(self):
        return not self.isfile

    def is_file(self):
        return self.isfile

    def stat(self):
        return os.stat(self.path)


"""
Base explorer window class, allows the user to navigate directories
"""


class explorer(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.title("Explorer")

        """
        Map to connect the string id's of the various nodes with layout:
        {
            {"entry" : DirEntry, "built" : False},
            {"entry" : DirEntry, "built" : False},
            ...
        }
        "built" indicates whether or not the node has been populated
        assuming it has children nodes.

        DirEntry is an object produced by the itterable os.scandir()
        It has several methods  it similar to those in the module os.path
        such as is_file, is_dir, and stat, and the object caches these
        values for later calls, resulting in better performance.

        The root node is mapped to "" and uses an artifical DirEntry.
        The rest are mapped to their string id's provided at the time of the node's creation.
        """
        self.node_map = {}

        self.style = Style(self)
        # Style treeview, not styling means
        # later calls to tag_configure() don't work
        self.style.map(
            "Treeview",
            foreground=[("disabled", "white")],
            background=[("disabled", "black")],
        )

        # If a path was passed set the current dir to it
        # Otherwise set it to the user's home dir
        if "path" in args:
            self.current_dir = kwargs.pop("path")
        else:
            self.current_dir = os.path.expanduser("~")

        self.set_title(self.current_dir)
        self.file_icon = load_tk_image_from_bytes_array(file_image_bytes)
        self.folder_icon = load_tk_image_from_bytes_array(folder_image_bytes)

        self.outer_frame = LabelFrame(self)
        self.outer_frame.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

        # Top row, frame to add a path to enter a path and button to go to it
        self.path_frame = Frame(self.outer_frame)
        self.path_frame.pack(side=tk.TOP, expand=0, fill="x")
        self.path_box = Entry(self.path_frame)
        self.path_box.pack(side=tk.LEFT, expand=1, fill=tk.BOTH, padx=5, pady=(1, 5))
        self.submit_path_button = Button(
            self.path_frame, text="⏎", command=self.submit_path
        )
        self.submit_path_button.pack(
            side=tk.CENTER, expand=0, fill=tk.BOTH, padx=(0, 4), pady=(0, 4)
        )  # Buttons have weird padding

        self.tree = ScrolledTree(self.outer_frame, columns=("size", "modified"))
        self.tree.pack(side=tk.TOP, expand=1, fill=tk.BOTH, padx=5, pady=(0, 5))
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<<TreeviewOpen>>", self.on_open)
        self.tree.column("#0", width=150)
        self.tree.column("size", width=60, minwidth=60, stretch="no")
        self.tree.column("modified", width=150, minwidth=150, stretch="no")
        self.tree.heading("#0", text="...", anchor="w")
        self.tree.heading("size", text="Size", anchor="w")
        self.tree.heading("modified", text="Modified", anchor="w")

        self.populate(self.current_dir)

    def set_title(self, string):
        self.title(f"TK Explorer - {string}")

    def submit_path(self):
        self.populate(self.tree.selection()[0])

    def on_open(self, event):
        # Get current node and attempt to build it
        # build_node will immediately return if already built
        self.build_node(self.tree.focus())

    def populate(self, dir: os.path):
        self.current_dir = dir
        self.node_map = {}  # Clear node map
        self.tree.delete(*self.tree.get_children())
        self.set_title(self.current_dir)
        self.build_tree()
        self.outer_frame.configure(text=self.current_dir)  # Set frame label text

    def build_tree(self):
        """Fills the tree with the contents of the path at self.current_dir"""
        # Create entry in the node map for the tree root
        self.node_map[""] = {"entry": DirEntry(self.current_dir), "built": False}
        self.build_node("")  # Build tree root

    def build_node(self, node: id):
        """"""
        node_dict = self.node_map[node]
        if node_dict["built"]:
            return

        path = node_dict["entry"]
        self.tree.delete(*self.tree.get_children(node))
        try:
            dir_items = os.scandir(path.path)
        except PermissionError:
            dir_items = []

        files, folders_then_both = [], []
        for entry in dir_items:  # Sort files from folders
            files.append(entry) if entry.is_file() else folders_then_both.append(entry)
        folders_then_both.extend(files)  # Sort folders-first
        for entry in folders_then_both:
            if entry.is_file():
                size = _sizeof_fmt(
                    os.path.getsize(entry.path)
                )  # Get friendly file size
                modified = _get_human_mtime(entry.path)  # Get human modified time
            else:
                size = ""
                modified = ""

            branch = self.tree.insert(
                node, "end", text=entry.name, values=(size, modified, "")
            )
            self.build_branch(branch, entry)  # Flesh out the branch
            # Built status is set to false if it's a dir since it may have children
            self.node_map[branch] = {"entry": entry, "built": entry.is_file()}

        self.node_map[node]["built"] = True

    def build_branch(self, branch: id, entry: DirEntry):
        # Flesh out an empty branch
        # Adds an image to the branch based on its type (file or folder)
        # Also adds a + to the node if it has children
        if entry.is_dir():
            try:
                self.tree.item(branch, image=self.folder_icon)
                if os.scandir(entry.path):
                    # Insert a single empty node in the branch.
                    # This is so the branch has a clickable +,
                    # when the + is clicked build_node(branch) is called.
                    # The empty node gets erased when build_node gets called.
                    self.tree.insert(branch, "end", text=".", values=("", "", ""))
            except PermissionError:  # make folder appear empty if no permission to access it
                print(entry.path)
                pass
        else:
            self.tree.item(branch, image=self.file_icon)

    def on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        column = self.tree.identify_column(event.x) == "#0"
        if region == "heading" and column:  # If clicking on the "..." on the top left
            self.populate(os.path.dirname(self.current_dir))
        else:
            node_dict = self.node_map[self.tree.selection()[0]]
            if node_dict["entry"].is_dir():
                self.populate(node_dict["entry"].path)


"""
Dialog class, configures the background color of nodes with valid/invalid tags.
This class isn't meant to be used directly.
Adds entry box at the bottom of the window to display the path represented by the 
currently selected node if the selected item (folder, file) is valid for return.
"""


class _dialog(explorer):
    def __init__(self, *args, **kwargs):
        explorer.__init__(self, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.title("base dialog")
        self.lift()  # Bring window to top
        self.focus_force()  # Force focus on window
        self.grab_set()  # Prevent other windows from being accessed
        self.tree.tag_configure(
            "invalid", foreground="dimgray"
        )  # configure invalid items for selection in the tree
        self.tree.tag_configure(
            "valid", foreground="black"
        )  # configure valid items for selection in the tree
        self.awaiting_selection = False  # See get_input
        self.canceled = False  # See get_input
        self.selection_made = False  # See get_input
        self.selection = None  # See get_input

    def get_input(self, input_type="file"):
        """
        Method to get an input from the dialog window.
        Sets the 'awaiting_selection' variable to true so
        the mainloop knows the window is expecting input.
        This method then waits until a selection has been
        made, which the mainloop indicates by setting
        self.selection_made to 'True'.
        The selection is then copied and the dialog window
        is destroyed, finally the result is returned to the
        function that call get_input.

        How self.selection and self.selection_made is set
        is different for each class built from _dialog

        Cancel is called whenever the window is closed to
        allow any thread waiting for a selection to be made
        to exit, as this normally prevents the script from
        being killed even with a keyboard interrupt
        """
        self.awaiting_selection = True
        while not self.selection_made and not self.canceled:
            pass
        if self.canceled:
            self.destroy()
            return
        selection = self.selection
        self.grab_release()
        self.destroy()
        return selection

    def cancel(self):
        self.canceled = True


"""
File dialog window
"""


class file_dialog(_dialog):
    def __init__(self, *args, **kwargs):
        self.endings = kwargs.pop("endings") if "endings" in kwargs else None
        _dialog.__init__(self, *args, **kwargs)
        self.set_title(self.current_dir)

    # Redefine set_title
    def set_title(self, string):
        """Adds a list of valid file endings to the window title"""
        end = " - [" + " , ".join(e for e in self.endings) + "]" if self.endings else ""
        self.title(f"Please select a file - {string}{end}")

    def build_branch(self, branch, entry):
        """Labels entries based on if they are valid for selection"""
        if entry.is_file():
            if self.endings:
                for ending in self.endings:
                    if entry.name.endswith(ending):
                        self.tree.item(branch, tags=("valid",))
                    else:
                        self.tree.item(branch, tags=("invalid",))
            else:
                self.tree.item(branch, tags=("valid",))
        else:
            self.tree.item(branch, tags=("invalid",))
        super().build_branch(branch, entry)

    """Add selection code for the underlying _explorer class
       If the item double-clicked is valid set selection to
       the entry's path and set the selection_made flag so
       the waiting thread knows to access the selection"""

    def on_double_click(self, event):
        if self.awaiting_selection:
            region = self.tree.identify("region", event.x, event.y)
            if not region == "heading":
                node_dict = self.node_map[self.tree.selection()[0]]
                if node_dict["entry"].is_file():
                    if self.endings:
                        for end in self.endings:
                            if node_dict["entry"].path.endswith(end):
                                self.selection = node_dict["entry"].path
                                self.selection_made = True
                    else:
                        self.selection = node_dict["entry"].path
                        self.selection_made = True
        super().on_double_click(event)


"""
Folder dialog window
"""


class folder_dialog(_dialog):
    def __init__(self, *args, **kwargs):
        _dialog.__init__(self, *args, **kwargs)
        self.title("Please select a folder")

    # Redefine set_title
    def set_title(self, string):
        self.title(f"Please select a folder - {string}")

    def build_branch(self, branch, entry):
        if entry.is_dir():
            self.tree.item(branch, tags=("valid",))
        else:
            self.tree.item(branch, tags=("invalid",))
        super().build_branch(branch, entry)

    def on_double_click(self, event):
        if self.awaiting_selection:
            region = self.tree.identify("region", event.x, event.y)
            if not region == "heading":
                node_dict = self.node_map[self.tree.selection()[0]]
                if node_dict["entry"].is_dir():
                    self.selection = node_dict["entry"].path
                    self.selection_made = True
        super().on_double_click(event)


##SCROLLING WIDGET STUFF
# Dual-inheritance support object
# Adds and hides scroll bars automatically around a widget
class ScrollWrapper(object):
    def __init__(self, container):
        self.grid(column=0, row=0, sticky="nsew")
        # Try to load vertical scroll bar, exception means one is not needed
        try:
            v_scrollbar = tk.Scrollbar(container, orient="vertical", command=self.yview)
            self.configure(yscrollcommand=self._ScrollWrapper(v_scrollbar))
            v_scrollbar.grid(column=1, row=0, sticky="ns")
        except:
            pass

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        methods = (
            tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() | tk.Place.__dict__.keys()
        )
        for m in methods:
            if m[0] != "_" and m not in ["config", "configure"]:
                setattr(self, m, getattr(container, m))

    @staticmethod
    def _ScrollWrapper(sbar):
        """Hide and show scrollbar automatically"""

        def wrap(begining, end):
            begining, end = float(begining), float(end)
            if begining <= 0 and end >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(begining, end)

        return wrap

    def __str__(self):
        return str(self.master)


def _create_frame(func):
    """Wraps widget and bars in frame and adds bindings"""

    def wrapped(cls, master, **kw):
        f = tk.Frame(master)
        f.bind("<Enter>", lambda e: _bind_mousewheel(e, f))
        f.bind("<Leave>", lambda e: _unbind_mousewheel(e, f))
        return func(cls, f, **kw)

    return wrapped


def _bind_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() in ["Windows", "Darwin"]:
        child.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, child))
        child.bind_all("<Shift-MouseWheel>", lambda e: _on_mousewheel(e, child))
    else:  # Linux
        child.bind_all("<Button-4>", lambda e: _on_mousewheel(e, child))
        child.bind_all("<Button-5>", lambda e: _on_mousewheel(e, child))
        child.bind_all("<Shift-Button-4>", lambda e: _on_mousewheel(e, child))
        child.bind_all("<Shift-Button-5>", lambda e: _on_mousewheel(e, child))


def _unbind_mousewheel(event, widget):
    if platform.system() in ["Windows", "Darwin"]:
        widget.unbind_all("<MouseWheel>")
        widget.unbind_all("<Shift-MouseWheel>")
    else:  # Linux
        widget.unbind_all("<Button-4>")
        widget.unbind_all("<Button-5>")
        widget.unbind_all("<Shift-Button-4>")
        widget.unbind_all("<Shift-Button-5>")


def _on_mousewheel(event, widget):
    if platform.system() == "Windows":
        widget.yview_scroll(-1 * int(event.delta / 120), "units")
    elif platform.system() == "Darwin":
        widget.yview_scroll(-1 * int(event.delta), "units")
    else:  # Linux
        if event.num == 4:
            widget.yview_scroll(-1, "units")
        elif event.num == 5:
            widget.yview_scroll(1, "units")


##END SCROLLING WIDGET STUFF

# Not Used. Function to create byte-encoded images for use with tkinter
# def convert_png_to_bytes_array(png_path):
#   bytes_array = io.BytesIO()
#   Image.open(png_path, mode="r").save(bytes_array, format="PNG")
#   return bytes_array.getvalue()

# Converts a png encoded in bytes to an image tkinter can process
def load_tk_image_from_bytes_array(bytes_array):
    return ImageTk.PhotoImage(Image.open(io.BytesIO(bytes_array)))


# Public domain code to convert file size in bytes to be friendly
def _sizeof_fmt(num, suffix="B"):
    divider = 1024  # 1000 for MiB
    for unit in ["", "k", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0


# Converts a unix timestamp to human-friendly time
def _get_human_mtime(path):
    return str(datetime.fromtimestamp(os.path.getmtime(path)))[:19]


if __name__ == "__main__":
    # The script / args are really just for demonstation / testing purposes
    # The primary use of this is as a module to modify / expand on for future projects
    # parser = argparse.ArgumentParser(description=desc)
    # exclusive = parser.add_mutually_exclusive_group(required=True)
    # exclusive.add_argument("-f", "--file", help = "Choose a file", action="store_true")
    # exclusive.add_argument("-d", "--dir", help = "Choose a dir", action="store_true")
    # exclusive.add_argument("-e", "--explorer", help = "Basic Explorer", action="store_true")
    # args = parser.parse_args()

    class Threader:
        """Simple threader to prevent get_input causing blocking"""

        def __init__(self, max_worker_threads: int = 3):
            self.threads = []

        def add_thread(self, callback, arglist: list = []):
            """Add a callback to be done as a thread with an optional arglist"""
            t = threading.Thread(target=callback, args=arglist)
            t.start()
            self.threads.append(t)
            return t

        def join(self):
            for t in threads:
                t.join()

    threader = Threader()

    # Simple gui to test the folder and file picker
    class test_gui(tk.Tk):
        def __init__(self, args, picker_type):
            tk.Tk.__init__(self)
            self.picker_type = picker_type
            self.title("test")
            self.geometry(f"{WIDTH}x{HEIGHT}")
            f = Frame(self)
            f.pack(expand=1, fill=tk.BOTH)
            self.l = Label(f, anchor="center")
            self.l.pack(side=tk.TOP, expand=1, fill=tk.BOTH)
            if args.file:
                text = "Pick a file!"
            elif args.dir:
                text = "Pick a folder!"
            else:  # Not used
                text = "Pick something!"

            Button(
                f,
                text=text,
                command=lambda: threader.add_thread(
                    self.get_input
                ),  # Lambda function to
            ).pack(expand=0, side=tk.BOTTOM)

        def get_input(self):
            dialog = self.picker_type(self)  # Make the dialog window
            selection = dialog.get_input()  #
            self.l.configure(text=selection)

    w = test_gui()

    # if args.file:
    #   w = test_gui(args, file_dialog)
    # elif args.dir:
    #   w = test_gui(args, folder_dialog)
    # elif args.explorer:
    #   w = explorer()
    # else:
    #   raise NotFound("No matching dialog found")

    w.mainloop()
