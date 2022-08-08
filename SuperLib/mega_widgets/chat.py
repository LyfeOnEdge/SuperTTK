# Todo:
# Option to add a new chat session tab
import os, time, json
import tkinter as tk
from tkinter import ttk, simpledialog, filedialog
import tkinter.font as tkFont

from .. import (
    Tab,
    ScrolledCanvas,
    LabeledEntry,
    LabeledButtonEntry,
    get_lorem_paragraphs,
    check_in_bounds,
    FocusedToplevel,
    get_generated_font_images_lookup,
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

# Causes circular input
from ..widgets.WidgetsCore import get_asset

FONTS = get_generated_font_images_lookup()


def load_icon(size, color, char):
    return tk.PhotoImage(file=FONTS[size][color][char])


BUBBLE_SIDE_SPACING = 60
SCROLLBAR_WIDTH = 15
BUBBLE_HEIGHT = 30
START_Y_PADDING = 10
BOTTOM_BAR_HEIGHT = 40
BOTTOM_BAR_Y_PADDING = 5
BOTTOM_BAR_X_PADDING = 10
BOTTOM_BAR_ENTRY_X_PADDING = 5
BUBBLE_Y_PADDING = 10
BUBBLE_X_PADDING = 20
TEXT_Y_PADDING = 10
TEXT_X_PADDING = 20
ICON_X_PADDING = 0
HOVER_WIDTH = 5
ACTION_ICON_PADDING = 5
MESSAGE_BORDER_WIDTH = 2
CONVERSATIONS_FOLDER = os.path.abspath("Conversations")
CONVERSATION_FILE_ENDING = "_meta.json"

def get_conversations_list():
    conversations = []
    for entry in os.scandir(CONVERSATIONS_FOLDER):
        if entry.is_file():
            if entry.path.endswith(CONVERSATION_FILE_ENDING):
                conversations.append(entry.path)
    print(f"Found {len(conversations)} conversations")
    return conversations


def convert_messages_to_html(conversation):
    generator = HTML_Generator()

    for m in conversation.messages:
        ts = get_friendly_time(m.timestamp, mode="all")
        generator.start_div()
        generator.add_center(ts)
        generator.add_bold(m.user)
        generator.add_paragraph(m.content)
        generator.end_div()
        generator.add_divider()
    return generator.assemble()


def convert_messages_to_txt(conversation):
    generator = TXT_Generator()
    generator.add_body_line(f"Conversation - {conversation.title}")
    for m in conversation.messages:
        ts = get_friendly_time(m.timestamp, mode="all")
        generator.add_body_line(m.user + f" @ {ts}")
        generator.add_body_line(m.content)
        generator.add_divider()
    return generator.assemble()


class Conversation:
    def __init__(self, title, atomic, messages=[]):
        self.title = title
        self.messages = messages
        self.atomic = atomic
        self.conversation_path = os.path.join(
            CONVERSATIONS_FOLDER, atomic + CONVERSATION_FILE_ENDING
        )

    def add_message(self, message):
        self.messages.append(message)
        self.save()

    def delete_message(self, message):
        self.messages.remove(message)
        self.save()

    def pin_message(self, message):
        message.pinned = True
        self.save()

    def unpin_message(self, message):
        message.pinned = False
        self.save()

    def toggle_pinned(self, message):
        message.pinned = not message.pinned
        self.save()

    def save(self, path=None):
        path = path or self.conversation_path
        metadata = {
            "atomic": self.atomic,
            "title": self.title,
            "messages": [m.to_json() for m in self.messages],
        }
        with open(path, "w+") as f:
            json.dump(metadata, f)

    def rename(self, title):
        """Returns false on invalid name"""
        if self.title:
            self.title = title
            self.save()
            return True
        else:
            return False

    def delete(self):
        os.remove(self.conversation_path)


class LoadedConversation(Conversation):
    def __init__(self, conversationstab, path):
        with open(path, "r") as f:
            meta_json = json.load(f)
        messages = [LoadedMessage(conversationstab, m) for m in meta_json["messages"]]
        Conversation.__init__(
            self,
            meta_json["title"],
            meta_json["atomic"],
            messages=messages,
        )


class MessageObject:
    def __init__(self, content, user, icon, timestamp, pinned=False, active=False):
        self.content = content
        self.user = user
        self.icon = icon
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
            "user": self.user,
            "timestamp": self.timestamp,
            "pinned": self.pinned,
        }


class LoadedMessage(MessageObject):
    def __init__(self, conversationstab, json_data):
        content = json_data["content"]
        user = json_data["user"]
        # icon = json_data["icon"]
        icon = conversationstab.get_user_icon(user)
        timestamp = json_data["timestamp"]
        pinned = json_data["pinned"]
        MessageObject.__init__(self, content, user, icon, timestamp, pinned)


class BaseBubbleTab(Tab):
    def __init__(self, notebook, manager, app, name, conversation):
        Tab.__init__(self, notebook, name)
        self.app = app
        self.manager = manager
        self.window = app.window
        self.conversation = conversation
        self.displayed_messages = [m for m in self.conversation.messages]
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
        self.icon_backer = tk.PhotoImage(file=get_asset("profile.png"))
        # self.icon_backer = tk.PhotoImage(file="../../assets/profile.png")
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
        self.on_message_left_click = None
        self.on_message_middle_click = None
        self.on_message_right_click = None
        self.user_colors = {"default": "#cccccc"}

    def refresh(self, _=None, __=None):
        self.canvas.delete("all")
        self.width = self.canvas_scroller.winfo_width()
        running_total_height = START_Y_PADDING
        max_line_width = self.width - BUBBLE_SIDE_SPACING - SCROLLBAR_WIDTH
        max_text_width = max_line_width - 2 * TEXT_Y_PADDING
        left_align = TEXT_X_PADDING + BUBBLE_X_PADDING
        right_align = self.width - SCROLLBAR_WIDTH
        icon_height = self.icon_backer.height()
        for m in self.displayed_messages:
            ico = self.canvas.create_image(
                (left_align + BUBBLE_SIDE_SPACING - TEXT_X_PADDING) / 2,
                running_total_height,
                image=self.icon_backer,
                anchor="n",
            )
            ico_width, ico_height = bbox_to_width_and_height(self.canvas.bbox(ico))
            monogram = self.canvas.create_image(
                (left_align + BUBBLE_SIDE_SPACING - TEXT_X_PADDING) / 2,
                running_total_height + ico_height / 2,
                image=m.icon,
                anchor="center",
            )
            name_text = self.canvas.create_text(
                left_align + BUBBLE_SIDE_SPACING,
                running_total_height + TEXT_Y_PADDING,
                text=m.user,
                fill="black",
                anchor="nw",
                width=max_text_width - BUBBLE_X_PADDING - TEXT_X_PADDING,
                font=self.app.bold_font,
            )
            b = self.canvas.bbox(name_text)
            name_width, name_height = b[2] - b[0], b[3] - b[1]
            text = self.canvas.create_text(
                left_align + BUBBLE_SIDE_SPACING,
                running_total_height + TEXT_Y_PADDING + name_height,
                text=m.content,
                fill="black",
                anchor="nw",
                width=max_text_width - BUBBLE_X_PADDING - TEXT_X_PADDING,
            )
            b = self.canvas.bbox(text)
            width, height = b[2] - b[0], b[3] - b[1]
            bg = self.canvas.create_round_rectangle(
                left_align + BUBBLE_SIDE_SPACING - TEXT_X_PADDING,
                running_total_height,
                right_align - TEXT_Y_PADDING,
                running_total_height + height + name_height + 2 * TEXT_Y_PADDING,
                fill=self.user_colors.get(m.user, self.user_colors.get("default")),
                width=MESSAGE_BORDER_WIDTH,
            )
            b = self.canvas.bbox(bg)
            bg_width, bg_height = b[2] - b[0], b[3] - b[1]
            m.set_position(b[0], b[1], bg_width, bg_height)
            height += name_height
            minsize = icon_height - 2 * TEXT_Y_PADDING
            running_total_height += height if height > minsize else minsize
            running_total_height += 2 * TEXT_Y_PADDING + BUBBLE_Y_PADDING
            self.canvas.tag_raise(name_text)
            self.canvas.tag_raise(text)
            self.canvas.tag_raise(ico)
            self.canvas.tag_raise(monogram)
            if m.active:
                self.activate_message(m)
        self.canvas_height = running_total_height
        self.canvas.config(
            scrollregion=(0, 0, running_total_height, running_total_height)
        )

    def deactivate_message(self, m):
        m.active = False
        for r in list(m.active_references.keys()):
            ref = m.active_references.pop(r)
            self.canvas.delete(ref)

    def activate_message(self, m):
        pass  # Override in subclass

    def _on_action(self, event, on_find_action=None):
        x, y = event.x, self.get_adjusted_y_view(event)
        found = False
        for m in self.conversation.messages:
            if not found:
                if m.is_in_range(x, y):
                    found = True
                    self.hovered = m
                    if not m.active and not m.no_redraw:
                        self.activate_message(m)
                    if on_find_action:
                        on_find_action(m)
                else:
                    self.deactivate_message(m)
            else:
                self.deactivate_message(m)
        if not found:
            self.hovered = None

    def on_mouse_move(self, event):
        self._on_action(event)

    def on_left_click(self, event):
        def on_left_click(message):
            if self.on_message_left_click:
                self.on_message_left_click(message)

        self._on_action(event, on_find_action=on_left_click)

    def on_left_click_release(self, event):
        self.refresh()

    def on_middle_click(self, event):
        def on_middle_click(message):
            if self.on_message_middle_click:
                self.on_message_middle_click(message)

        self._on_action(event, on_find_action=on_middle_click)

    def on_right_click(self, event):
        def on_right_click(message):
            if self.on_message_right_click:
                self.on_message_right_click(message)

        self._on_action(event, on_find_action=on_right_click)

    def get_adjusted_y_view(self, event):
        return int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))


class PinnedMessagesTab(BaseBubbleTab):  # Init after chat tab
    def __init__(self, notebook, manager, app):
        BaseBubbleTab.__init__(
            self, notebook, manager, app, "Pinned", manager.chat_tab.conversation
        )

    def refresh(self, _=None, __=None):
        self.displayed_messages = []
        for m in self.conversation.messages:
            if m.pinned:
                self.displayed_messages.append(m)
        BaseBubbleTab.refresh(self)


class ChatTab(BaseBubbleTab):
    def __init__(self, notebook, manager, controller, app, conversation):
        BaseBubbleTab.__init__(self, notebook, manager, app, "Chat", conversation)
        self.controller = controller
        self.user_colors = {
            "Technician": "#b1d5de",
            "default": "#cccccc",
        }

        bottom_bar = ttk.Frame(self)
        bottom_bar.place(
            height=BOTTOM_BAR_HEIGHT, relwidth=1, rely=1, y=-BOTTOM_BAR_HEIGHT
        )

        self.left_entry = LabeledEntry(
            bottom_bar,
            labeltext="Technician",
            bind_enter=True,
            command=self.add_left_message,
        )

        self.left_entry.pack(
            expand=True,
            fill="both",
            side=tk.LEFT,
            padx=(BOTTOM_BAR_X_PADDING, BOTTOM_BAR_ENTRY_X_PADDING),
            pady=BOTTOM_BAR_Y_PADDING,
        )

        self.right_entry = LabeledEntry(
            bottom_bar,
            labeltext="End User",
            bind_enter=True,
            command=self.add_right_message,
        )
        self.right_entry.pack(
            expand=True,
            fill="both",
            side=tk.RIGHT,
            padx=(BOTTOM_BAR_ENTRY_X_PADDING, BOTTOM_BAR_X_PADDING),
            pady=BOTTOM_BAR_Y_PADDING,
        )

        def focus_left(event=None):
            self.left_entry.focus()
            return "break"

        self.right_entry.bind("<Tab>", focus_left)
        app.window.update_idletasks()  # forces draw so canvas displays correctly
        self.refresh()

    def refresh(self, _=None, __=None):
        self.displayed_messages = self.conversation.messages
        BaseBubbleTab.refresh(self)

    def on_left_click(self, event):  # Override superclass
        pos = event.x, self.get_adjusted_y_view(event)

        def on_left_click(message):  # If a message was clicked, check its subregions
            m = message
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
                self.manager.delete_message(message)
            elif m.active_references.get("pin") and check_in_bounds(
                pos, self.canvas.bbox(m.active_references["pin"])
            ):
                self.conversation.toggle_pinned(m)
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

    def add_left_message(self, message):
        if message:
            self.conversation.add_message(
                MessageObject(
                    message,
                    "Technician",
                    self.controller.get_user_icon("Technician"),
                    time.time(),
                )
            )
        self.left_entry.clear()
        self.refresh()
        self.canvas.yview_moveto(1)

    def add_right_message(self, message):
        if message:
            self.conversation.add_message(
                MessageObject(
                    message,
                    "End User",
                    self.controller.get_user_icon("End User"),
                    time.time(),
                )
            )
        self.right_entry.clear()
        self.refresh()
        self.canvas.yview_moveto(1)

    def activate_message(self, m):
        if m.active:
            self.deactivate_message(m)
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

        dat = self.canvas.create_text(
            m.x + m.width / 2,
            m.y + 1,
            text=get_friendly_time(m.timestamp, mode="date"),
            fill="black",
            anchor="n",
            font=self.app.small_bold_font,
        )
        tim = self.canvas.create_text(
            m.x + m.width / 2,
            self.canvas.bbox(dat)[3],
            text=get_friendly_time(m.timestamp, mode="time"),
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
                "date": dat,
                "time": tim,
            }
        )


class OptionsTab(Tab):
    def __init__(self, notebook, conversationstab, convotab, app):
        Tab.__init__(self, notebook, "Options")
        self.conversationstab = conversationstab
        self.notebook = notebook
        self.convotab = convotab

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

        convo_options = (
            (
                "Rename Conversation",
                lambda: conversationstab.rename_conversation(convotab.conversation),
            ),
            (
                "Copy Conversation",
                lambda: conversationstab.copy_conversation(convotab.conversation),
            ),
            (
                "Delete Conversation",
                lambda: conversationstab.delete_conversation(convotab.conversation),
            ),
        )
        build_button_menu("Conversation Options", convo_options)
        export_options = (
            (
                "Export to HTML",
                lambda: conversationstab.export_conversation_html(
                    convotab.conversation
                ),
            ),
            # ("Export to MD", dummy_function),
            (
                "Export to TXT",
                lambda: conversationstab.export_conversation_text(
                    convotab.conversation
                ),
            ),
            (
                "Export to JSON",
                lambda: conversationstab.export_conversation_json(
                    convotab.conversation
                ),
            ),
        )
        build_button_menu("Export Options", export_options)


class ConvoTab(Tab):
    def __init__(self, notebook, app, conversationstab, conversation):
        Tab.__init__(self, notebook, conversation.title)
        self.conversation = conversation
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.chat_tab = ChatTab(
            self.notebook, self, conversationstab, app, conversation
        )
        self.pinned_tab = PinnedMessagesTab(self.notebook, self, app)
        self.options_tab = OptionsTab(self.notebook, conversationstab, self, app)
        self.conversationstab = conversationstab

    def delete_message(self, message):
        if message.pinned:
            self.conversation.unpin_message(message)
        self.pinned_tab.refresh()
        self.conversation.delete_message(message)

    def rename_conversation(self, title):
        self.conversationstab.notebook.tab(self, text=title)
        self.conversation.rename(title)


class ConversationsTab(Tab):
    def __init__(self, notebook, app):
        self.app = app
        os.makedirs(CONVERSATIONS_FOLDER, exist_ok=True)
        Tab.__init__(self, notebook, "Conversations")
        self.cached_icons = {}
        self.toplevel = None
        self.load_conversations()
        conversation_menu = tk.Menu(self.app.menu, tearoff=0)
        conversation_menu.add_command(
            label="New conversation", command=self.new_conversation
        )
        conversation_menu.add_command(
            label="Refresh conversations", command=self.reload_conversations
        )
        self.app.menu.add_cascade(menu=conversation_menu, label="Conversations")

    def reload_conversations(self):
        self.notebook.destroy()
        self.load_conversations()

    def load_conversations(self):
        self.tabs = {}
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        for convo_path in get_conversations_list():
            convo = LoadedConversation(self, convo_path)
            self.tabs[convo] = ConvoTab(self.notebook, self.app, self, convo)
        self.app.window.update_idletasks()
        self.app.use_theme(self.app.current_theme)

    def get_cached_icon(self, size, color, char):
        size = int(size)
        if not size in self.cached_icons:
            self.cached_icons[size] = {}
        if not color in self.cached_icons[size]:
            self.cached_icons[size][color] = {}
        if not char in self.cached_icons[size][color]:
            self.cached_icons[size][color][char] = load_icon(size, color, char)
        return self.cached_icons[size][color][char]

    def get_user_icon(self, user):
        return self.get_cached_icon(32, "white", user[0])

    def new_conversation(self, event=None):
        if self.toplevel:
            self.toplevel.destroy()
            self.toplevel = None

        self.toplevel = PromptWindow(
            window=self.app.window,
            text="Enter New Conversation Name:",
            on_yes=self.start_new_conversation,
            yes_text="Create Conversation",
            on_cancel=self.on_toplevel_destroy,
            no_destroy=True,
        )

    def start_new_conversation(self, title=None):
        if not title:
            self.toplevel.label_var.set("Enter valid conversation title")
            return
        self.toplevel.destroy()
        self.toplevel = None
        self.app.window.update_idletasks()
        self.make_new_conversation(title)

    def make_new_conversation(self, title):
        while not title and not title is None:
            title = simpledialog.askstring(
                title="New Conversation",
                prompt="Invalid Title, Please Enter a Valid Conversation Title: ",
            )
        if title is None:
            return
        timestamp = get_unix_timestring()
        last_tab = self.notebook.index("end")
        convo = Conversation(title, timestamp)
        convo.save()
        self.tabs[convo] = ConvoTab(self.notebook, self.app, self, convo)
        self.app.use_theme(self.app.current_theme)
        self.notebook.select(last_tab)
        self.app.notebook.select(self.app.notebook.index(self))

    def on_toplevel_destroy(self, *args):
        """Function for toplevels to call on no / cancel"""
        self.toplevel.destroy()

    def rename_conversation(self, conversation):
        tab = self.tabs[conversation]

        def do_rename(new_name):
            if not new_name:
                self.toplevel.label_var.set("Enter valid conversation title")
                return
            tab.rename_conversation(new_name)
            self.toplevel.destroy()

        self.toplevel = PromptWindow(
            window=self.app.window,
            text="Enter New Conversation Name:",
            yes_text="Rename",
            on_yes=do_rename,
            on_cancel=self.on_toplevel_destroy,
            no_destroy=True,
        )

    def copy_conversation(self, conversation):
        tab = self.tabs[conversation]

        def do_copy(new_name):
            if not new_name:
                self.toplevel.label_var.set("Enter valid conversation title")
                return
            new_conversation = Conversation(
                new_name, get_unix_timestring(), conversation.messages
            )
            new_conversation.save()
            self.reload_conversations()
            self.toplevel.destroy()

        self.toplevel = PromptWindow(
            window=self.app.window,
            text="Enter Conversation Copy Name:",
            yes_text="Make Copy",
            on_yes=do_copy,
            on_cancel=self.on_toplevel_destroy,
            no_destroy=True,
        )
        self.toplevel.var.set(conversation.title + " - Copy")

    def delete_conversation(self, conversation):
        tab = self.tabs[conversation]

        def do_delete(_=None):
            conversation.delete()
            self.reload_conversations()
            self.toplevel.destroy()

        self.toplevel = YesNoCancelWindow(
            window=self.app.window,
            text=f'Are you sure you want to delete "{conversation.title}" ?',
            on_yes=do_delete,
            on_cancel=self.on_toplevel_destroy,
            yes_text="Confirm Delete",
            no_destroy=True,
            no_enabled=False,
        )

    def export_conversation_html(self, conversation):
        html = convert_messages_to_html(conversation)
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

    def export_conversation_markdown(self, conversation):
        pass

    def export_conversation_text(self, conversation):
        text = convert_messages_to_txt(conversation)
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

    def export_conversation_json(self, conversation):
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
            conversation.save(filename)
