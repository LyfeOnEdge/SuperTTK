import os, time, json
import tkinter as tk
from tkinter import ttk, simpledialog, filedialog
import tkinter.font as tkFont

from .. import (
    Tab,
    ScrolledCanvas,
    LabeledEntry,
    get_lorem_paragraphs,
    check_in_bounds,
    FocusedToplevel,
    get_unix_timestring,
    HTML_Generator,
    dummy_function,
    center_window,
    PromptWindow,
    YesNoCancelWindow,
    bbox_to_width_and_height,
    TXT_Generator,
    get_user_home_folder,
    get_friendly_time,
)

from ..widgets.WidgetsCore import get_asset


def convert_notes_to_html(note):
    generator = HTML_Generator()
    for m in note.notes:
        ts = get_friendly_time(m.timestamp, mode="all")
        generator.start_div()
        generator.add_center(ts)
        generator.add_paragraph(m.content)
        generator.end_div()
        generator.add_divider()
    return generator.assemble()


def convert_notes_to_txt(note):
    generator = TXT_Generator()
    generator.add_body_line(f"Note - {note.title}")
    for m in note.notes:
        ts = get_friendly_time(m.timestamp, mode="all")
        generator.add_body_line(m.content)
        generator.add_divider()
    return generator.assemble()


BUBBLE_SIDE_SPACING = 20
SCROLLBAR_WIDTH = 15
BUBBLE_HEIGHT = 30
START_Y_PADDING = 10
BOTTOM_BAR_HEIGHT = 40
BOTTOM_BAR_Y_PADDING = 5
BOTTOM_BAR_X_PADDING = 10
BOTTOM_BAR_ENTRY_X_PADDING = 5
BUBBLE_Y_PADDING = 10
BUBBLE_X_PADDING = 10
TEXT_Y_PADDING = 10
TEXT_X_PADDING = 10
ICON_X_PADDING = 0
HOVER_WIDTH = 5
ACTION_ICON_PADDING = 5
MESSAGE_BORDER_WIDTH = 2
NOTES_FOLDER = os.path.abspath("Notes")
NOTE_FILE_ENDING = "_meta.json"
os.makedirs(NOTES_FOLDER, exist_ok=True)


def get_notes_list():
    notes = []
    for entry in os.scandir(NOTES_FOLDER):
        if entry.is_file():
            if entry.path.endswith(NOTE_FILE_ENDING):
                notes.append(entry.path)
    print(f"Found {len(notes)} notes")
    return notes


class Notepad:
    def __init__(self, title, atomic, notes=[]):
        self.title, self.atomic, self.notes = title, atomic, notes
        self.note_path = os.path.join(NOTES_FOLDER, atomic + NOTE_FILE_ENDING)

    def add_note(self, note):
        self.notes.append(note)
        self.save()

    def delete_note(self, note):
        self.notes.remove(note)
        self.save()

    def pin_note(self, note):
        note.pinned = True
        self.save()

    def unpin_note(self, note):
        note.pinned = False
        self.save()

    def toggle_pinned(self, note):
        note.pinned = not note.pinned
        self.save()

    def save(self, path=None):
        path = path or self.note_path
        metadata = {
            "atomic": self.atomic,
            "title": self.title,
            "notes": [m.to_json() for m in self.notes],
        }
        try:
            with open(path, "w+") as f:
                json.dump(metadata, f)
            return True
        except:
            return False

    def rename(self, title):
        """Returns false on invalid name"""
        if self.title:
            self.title = title
            return self.save()
        else:
            return False

    def delete(self):
        os.remove(self.note_path)


class LoadedNotepad(Notepad):
    def __init__(self, notestab, path):
        with open(path, "r") as f:
            meta_json = json.load(f)
        notes = [
            NoteEntry(m["content"], m["timestamp"], m["pinned"])
            for m in meta_json["notes"]
        ]
        Notepad.__init__(
            self,
            meta_json["title"],
            meta_json["atomic"],
            notes=notes,
        )


class NoteEntry:
    def __init__(self, content, timestamp, pinned=False, active=False):
        self.content = content
        self.timestamp = timestamp
        self.references = []
        self.active_references = {}
        self.active = active
        self.pinned = pinned
        self.x, self.y, self.width, self.height = 0, 0, 0, 0
        self.bbox = (0, 0, 0, 0)
        self.no_redraw = False

    def set_position(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.bbox = (self.x, self.y, self.x + self.width, self.y + self.height)

    def is_in_range(self, x, y):
        lb, tb, rb, bb = self.bbox
        return all((x > lb, x < rb, y > tb, y < bb))

    def to_json(self):
        return {
            "content": self.content,
            "timestamp": self.timestamp,
            "pinned": self.pinned,
        }


class BaseBubbleTab(Tab):
    def __init__(self, notebook, manager, app, name, notepad):
        Tab.__init__(self, notebook, name)
        self.app = app
        self.manager = manager
        self.window = app.window
        self.notepad = notepad
        self.displayed_notes = [m for m in self.notepad.notes]
        self.canvas_scroller = ScrolledCanvas(
            self, self.refresh, on_configure=self.refresh
        )
        self.canvas_scroller.place(relwidth=1, relheight=1, height=-BOTTOM_BAR_HEIGHT)
        self.canvas = self.canvas_scroller.canvas
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_click_release)
        self.canvas.bind("<Button-2>", self.on_middle_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.trash_icon = tk.PhotoImage(file=get_asset("trash_32_black.png"))
        self.clicked_trash_icon = tk.PhotoImage(file=get_asset("trash_32_white.png"))
        self.pin_icon = tk.PhotoImage(
            file=get_asset("pushpin_32_transparent_black.png")
        )
        self.clicked_pin_icon = tk.PhotoImage(
            file=get_asset("pushpin_32_transparent_white.png")
        )
        self.active_pin_icon = tk.PhotoImage(
            file=get_asset("pushpin_32_active_transparent_black.png")
        )
        self.active_clicked_pin_icon = tk.PhotoImage(
            file=get_asset("pushpin_32_active_transparent_white.png")
        )
        self.copy_icon = tk.PhotoImage(
            file=get_asset("copy_clipboard_32_plain_black_bold_arrow.png")
        )
        self.clicked_copy_icon = tk.PhotoImage(
            file=get_asset("copy_clipboard_32_plain_white_bold_arrow.png")
        )
        self.on_note_left_click = None
        self.on_note_middle_click = None
        self.on_note_right_click = None

    def refresh(self, _=None, __=None):
        self.canvas.delete("all")
        self.width = self.canvas_scroller.winfo_width()
        running_total_height = START_Y_PADDING
        max_line_width = self.width - SCROLLBAR_WIDTH
        max_text_width = max_line_width - 2 * TEXT_X_PADDING
        for m in self.displayed_notes:
            text = self.canvas.create_text(
                BUBBLE_SIDE_SPACING,
                running_total_height + TEXT_Y_PADDING,
                text=m.content,
                fill="black",
                anchor="nw",
                width=max_text_width - BUBBLE_X_PADDING - TEXT_X_PADDING,
            )
            b = self.canvas.bbox(text)
            width, height = b[2] - b[0], b[3] - b[1]
            bg = self.canvas.create_round_rectangle(
                BUBBLE_SIDE_SPACING - TEXT_X_PADDING,
                running_total_height,
                max_line_width - TEXT_Y_PADDING,
                running_total_height + height + 2 * TEXT_Y_PADDING,
                fill="#b1d5de",
                width=MESSAGE_BORDER_WIDTH,
            )
            b = self.canvas.bbox(bg)
            bg_width, bg_height = b[2] - b[0], b[3] - b[1]
            m.set_position(b[0], b[1], bg_width, bg_height)
            minsize = 2 * TEXT_Y_PADDING
            running_total_height += height if height > minsize else minsize
            running_total_height += 2 * TEXT_Y_PADDING + BUBBLE_Y_PADDING
            self.canvas.tag_raise(text)
            if m.active:
                self.activate_note(m)
        self.canvas_height = running_total_height
        self.canvas.config(
            scrollregion=(0, 0, running_total_height, running_total_height)
        )

    def deactivate_note(self, m):
        m.active = False
        for r in list(m.active_references.keys()):
            ref = m.active_references.pop(r)
            self.canvas.delete(ref)

    def activate_note(self, m):
        pass  # Override in subclass

    def _on_action(self, event, on_find_action=None):
        x, y = event.x, self.get_adjusted_y_view(event)
        found = False
        for m in self.notepad.notes:
            if not found:
                if m.is_in_range(x, y):
                    found = True
                    self.hovered = m
                    if not m.active and not m.no_redraw:
                        self.activate_note(m)
                    if on_find_action:
                        on_find_action(m)
                else:
                    self.deactivate_note(m)
            else:
                self.deactivate_note(m)
        if not found:
            self.hovered = None

    def on_mouse_move(self, event):
        self._on_action(event)

    def on_left_click(self, event):
        def on_left_click(note):
            if self.on_note_left_click:
                self.on_note_left_click(note)

        self._on_action(event, on_find_action=on_left_click)

    def on_left_click_release(self, event):
        self.refresh()

    def on_middle_click(self, event):
        def on_middle_click(note):
            if self.on_note_middle_click:
                self.on_note_middle_click(note)

        self._on_action(event, on_find_action=on_middle_click)

    def on_right_click(self, event):
        def on_right_click(note):
            if self.on_note_right_click:
                self.on_note_right_click(note)

        self._on_action(event, on_find_action=on_right_click)

    def get_adjusted_y_view(self, event):
        return int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))


class PinnedNotesTab(BaseBubbleTab):
    def __init__(self, notebook, manager, app):
        BaseBubbleTab.__init__(
            self, notebook, manager, app, "Pinned", manager.note_tab.notepad
        )

    def refresh(self, _=None, __=None):
        self.displayed_notes = []
        for m in self.notepad.notes:
            if m.pinned:
                self.displayed_notes.append(m)
        BaseBubbleTab.refresh(self)


class NoteTab(BaseBubbleTab):
    def __init__(self, notebook, manager, controller, app, notepad):
        BaseBubbleTab.__init__(self, notebook, manager, app, "Notepad", notepad)
        self.controller = controller

        bottom_bar = ttk.Frame(self)
        bottom_bar.place(
            height=BOTTOM_BAR_HEIGHT, relwidth=1, rely=1, y=-BOTTOM_BAR_HEIGHT
        )

        self.entry = LabeledEntry(
            bottom_bar,
            labeltext="Add Note: ",
            bind_enter=True,
            command=self.add_note,
        )
        self.entry.pack(expand=True, fill="both", side=tk.LEFT)
        ttk.Button(
            bottom_bar,
            text="Submit",
            command=self.add_note,
        ).pack(fill="y", side=tk.RIGHT)
        app.window.update_idletasks()  # forces draw so canvas displays correctly
        self.refresh()

    def refresh(self, _=None, __=None):
        self.displayed_notes = self.notepad.notes
        BaseBubbleTab.refresh(self)

    def on_left_click(self, event):  # Override superclass
        pos = event.x, self.get_adjusted_y_view(event)

        def on_left_click(note):  # If a note was clicked, check its subregions
            m = note
            if m.active_references.get("trash") and check_in_bounds(
                pos, self.canvas.bbox(m.active_references["trash"])
            ):
                ref = m.active_references.pop("trash")
                self.canvas.delete(ref)
                m.active_references["trash"] = self.canvas.create_image(
                    m.x + m.width - ACTION_ICON_PADDING,
                    m.y + 2 * ACTION_ICON_PADDING,
                    image=self.clicked_trash_icon,
                    anchor="ne",
                )
                self.manager.delete_note(note)
            elif m.active_references.get("pin") and check_in_bounds(
                pos, self.canvas.bbox(m.active_references["pin"])
            ):
                self.notepad.toggle_pinned(m)
                self.manager.pinned_tab.refresh()
                ref = m.active_references.pop("pin")
                self.canvas.delete(ref)
                b = self.canvas.bbox(m.active_references["trash"])
                img = [self.clicked_pin_icon, self.active_clicked_pin_icon][m.pinned]
                m.active_references["pin"] = self.canvas.create_image(
                    *b[:2],
                    image=img,
                    anchor="ne",
                )
            elif m.active_references.get("copy") and check_in_bounds(
                pos, self.canvas.bbox(m.active_references["copy"])
            ):
                ref = m.active_references.pop("copy")
                self.canvas.delete(ref)
                b = self.canvas.bbox(m.active_references["pin"])
                m.active_references["copy"] = self.canvas.create_image(
                    *b[:2],
                    image=self.clicked_copy_icon,
                    anchor="ne",
                )
                self.app.copy_to_user_clipboard(m.content)

        self._on_action(event, on_find_action=on_left_click)

    def add_note(self, text=None):
        if not text:
            text = self.entry.get()
        if text:
            self.notepad.add_note(
                NoteEntry(
                    text,
                    time.time(),
                )
            )
        self.entry.clear()
        self.refresh()
        self.canvas.yview_moveto(1)

    def activate_note(self, m):
        if m.active:
            self.deactivate_note(m)
        m.active = True

        trash = self.canvas.create_image(
            m.x + m.width - ACTION_ICON_PADDING,
            m.y + 2 * ACTION_ICON_PADDING,
            image=self.trash_icon,
            anchor="ne",
        )
        pin = self.canvas.create_image(
            *self.canvas.bbox(trash)[:2],
            image=self.active_pin_icon if m.pinned else self.pin_icon,
            anchor="ne",
        )
        copy = self.canvas.create_image(
            *self.canvas.bbox(pin)[:2],
            image=self.copy_icon,
            anchor="ne",
        )

        datetime = self.canvas.create_text(
            m.x + m.width / 2,
            m.y + 1,
            text=get_friendly_time(int(m.timestamp), mode="all"),
            fill="black",
            anchor="n",
            font=self.app.small_bold_font,
        )
        m.active_references.update(
            {
                "trash": trash,
                "pin": pin,
                "copy": copy,
                "outline": self.canvas.create_round_rectangle(
                    *m.bbox, width=HOVER_WIDTH
                ),
                "datetime": datetime,
            }
        )


class OptionsTab(Tab):
    def __init__(self, notebook, notestab, notepadtab, app):
        Tab.__init__(self, notebook, "Options")
        self.notestab = notestab
        self.notebook = notebook
        self.notepadtab = notepadtab

        def build_button_menu(title, options):
            options_frame = ttk.Labelframe(self, text=title)
            options_frame.pack(side=tk.TOP, fill="x", padx=10, pady=0)
            for opt in options:
                title, action = opt
                ttk.Button(
                    options_frame, text=title, command=action, padding=(0, 0)
                ).pack(
                    side=tk.TOP,
                    padx=10,
                    fill="x",
                    expand=True,
                    ipadx=0,
                    ipady=0,
                )

        notepad_options = (
            (
                "Rename Notepad",
                lambda: notestab.rename_note(notepadtab.notepad),
            ),
            (
                "Copy Notepad",
                lambda: notestab.copy_note(notepadtab.notepad),
            ),
            (
                "Delete Notepad",
                lambda: notestab.delete_note(notepadtab.notepad),
            ),
        )
        build_button_menu("Note Options", notepad_options)
        export_options = (
            (
                "Export to HTML",
                lambda: notestab.export_note_html(notepadtab.notepad),
            ),
            # ("Export to MD", dummy_function),
            (
                "Export to TXT",
                lambda: notestab.export_note_text(notepadtab.notepad),
            ),
            (
                "Export to JSON",
                lambda: notestab.export_note_json(notepadtab.notepad),
            ),
        )
        build_button_menu("Export Options", export_options)


class NotepadTab(Tab):
    def __init__(self, notebook, app, notestab, notepad):
        Tab.__init__(self, notebook, notepad.title)
        self.notepad = notepad
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.note_tab = NoteTab(self.notebook, self, notestab, app, notepad)
        self.pinned_tab = PinnedNotesTab(self.notebook, self, app)
        self.options_tab = OptionsTab(self.notebook, notestab, self, app)
        self.notestab = notestab

    def pin_note(self, note):
        if note.pinned:
            self.notepad.unpin_note(note)
        self.notepad.pin_note(note)
        self.pinned_tab.refresh()

    def delete_note(self, note):
        if note.pinned:
            self.notepad.unpin_note(note)
        self.pinned_tab.refresh()
        self.notepad.delete_note(note)

    def rename_note(self, title):
        self.notestab.notebook.tab(self, text=title)
        self.notepad.rename(title)


class NotesTab(Tab):
    def __init__(self, notebook, app):
        self.app = app
        Tab.__init__(self, notebook, "Notes")
        self.toplevel = None
        self.load_notes()
        note_menu = tk.Menu(self.app.menu, tearoff=0)
        note_menu.add_command(label="New Notepad", command=self.new_note)
        note_menu.add_command(label="Refresh notes", command=self.reload_notes)
        self.app.menu.add_cascade(menu=note_menu, label="Notes")

    def reload_notes(self):
        self.notebook.destroy()
        self.load_notes()

    def load_notes(self):
        self.tabs = {}
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        for notepad_path in get_notes_list():
            notepad = LoadedNotepad(self, notepad_path)
            self.tabs[notepad] = NotepadTab(self.notebook, self.app, self, notepad)
        self.app.window.update_idletasks()
        self.app.use_theme(self.app.current_theme)

    def new_note(self, event=None):
        if self.toplevel:
            self.toplevel.destroy()
            self.toplevel = None

        self.toplevel = PromptWindow(
            window=self.app.window,
            text="Enter New Notepad Name:",
            on_yes=self.start_new_note,
            yes_text="Create Notepad",
            on_cancel=self.on_toplevel_destroy,
            no_destroy=True,
        )

    def start_new_note(self, title=None):
        if not title:
            self.toplevel.label_var.set("Enter valid notepad title")
            return
        self.toplevel.destroy()
        self.toplevel = None
        self.app.window.update_idletasks()
        self.make_new_note(title)

    def make_new_note(self, title):
        while not title and not title is None:
            title = simpledialog.askstring(
                title="New Note",
                prompt="Invalid Title, Please Enter a Valid Notepad Title: ",
            )
        if title is None:
            return
        timestamp = get_unix_timestring()
        last_tab = self.notebook.index("end")
        convo = Notepad(title, timestamp)
        convo.save()
        self.tabs[convo] = NotepadTab(self.notebook, self.app, self, convo)
        self.app.use_theme(self.app.current_theme)
        self.notebook.select(last_tab)
        self.app.notebook.select(self.app.notebook.index(self))

    def on_toplevel_destroy(self, *args):
        """Function for toplevels to call on no / cancel"""
        self.toplevel.destroy()

    def rename_note(self, note):
        tab = self.tabs[note]

        def do_rename(new_name):
            if not new_name:
                self.toplevel.label_var.set("Enter valid notepad title")
                return
            tab.rename_note(new_name)
            self.toplevel.destroy()

        self.toplevel = PromptWindow(
            window=self.app.window,
            text="Enter New Notepad Name:",
            yes_text="Rename",
            on_yes=do_rename,
            on_cancel=self.on_toplevel_destroy,
            no_destroy=True,
        )

    def copy_note(self, note):
        tab = self.tabs[note]

        def do_copy(new_name):
            if not new_name:
                self.toplevel.label_var.set("Enter valid notepad title")
                return
            new_note = Notepad(new_name, get_unix_timestring(), note.notes)
            new_note.save()
            self.reload_notes()
            self.toplevel.destroy()

        self.toplevel = PromptWindow(
            window=self.app.window,
            text="Enter Notepad Copy Name:",
            yes_text="Make Copy",
            on_yes=do_copy,
            on_cancel=self.on_toplevel_destroy,
            no_destroy=True,
        )
        self.toplevel.var.set(note.title + " - Copy")

    def delete_note(self, note):
        tab = self.tabs[note]

        def do_delete(_=None):
            note.delete()
            self.reload_notes()
            self.toplevel.destroy()

        self.toplevel = YesNoCancelWindow(
            window=self.app.window,
            text=f'Are you sure you want to delete "{note.title}" ?',
            on_yes=do_delete,
            on_cancel=self.on_toplevel_destroy,
            yes_text="Confirm Delete",
            no_destroy=True,
            no_enabled=False,
        )

    def export_note_html(self, note):
        html = convert_notes_to_html(note)
        filetypes = [
            ("HTML Files", "*.html"),
            ("All Files", "*.*"),
        ]
        filename = filedialog.asksaveasfilename(
            parent=self.app.window,
            defaultextension=filetypes,
            filetypes=filetypes,
            initialdir=get_user_home_folder(),
        )
        if filename:
            with open(filename, "w+") as f:
                f.write(html)

    def export_note_markdown(self, note):
        pass

    def export_note_text(self, note):
        text = convert_notes_to_txt(note)
        filetypes = [
            ("TXT Files", "*.txt"),
            ("All Files", "*.*"),
        ]
        filename = filedialog.asksaveasfilename(
            parent=self.app.window,
            defaultextension=filetypes,
            filetypes=filetypes,
            initialdir=get_user_home_folder(),
        )
        if filename:
            with open(filename, "w+") as f:
                f.write(text)

    def export_note_json(self, note):
        filetypes = [
            ("JSON Files", "*.json"),
            ("All Files", "*.*"),
        ]
        filename = filedialog.asksaveasfilename(
            parent=self.app.window,
            defaultextension=filetypes,
            filetypes=filetypes,
            initialdir=get_user_home_folder(),
        )
        if filename:
            note.save(filename)
