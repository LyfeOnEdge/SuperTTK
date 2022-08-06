from .widgets.WidgetsCore import (
    bbox_to_width_and_height,
    center_window,
    check_in_bounds,
    complex_widget_search,
    copy_to_user_clipboard,
    CORE_FUNCTIONS,
    CORE_OBJECTS,
    create_round_rectangle,
    default_pack,
    default_separator,
    default_vertical_pack,
    default_vertical_separator,
    enable_notebook_movement,
    force_aspect,
    get_asset,
    get_bundled_themes_list,
    get_generated_font_images_lookup,
    get_themes_folder,
    open_link,
    recursive_widget_search,
    run_cl,
    SuperWidgetMixin,
    WINDOWS_SYMBOL,
)
from .widgets.Tabs import (
    Tab,
    LauncherTab,
    BrowserLauncherTab,
    CommandLauncherTab,
    ConsoleTab,
    TableTab,
    TreeTableTab,
    TABS,
)
from .widgets.CheckbuttonWidgets import (
    LabeledCheckbutton,
    LabeledMultiCheckbutton,
    CHECKBUTTON_WIDGETS,
)
from .widgets.ComboboxWidgets import (
    LabeledCombobox,
    LabeledMultiCombobox,
    COMBOBOX_WIDGETS,
)
from .widgets.OptionMenuWidgets import (
    LabeledOptionMenu,
    LabeledMultiOptionMenu,
    OPTIONMENU_WIDGETS,
)
from .widgets.EntryWidgets import (
    LabeledEntry,
    LabeledMultiEntry,
    LabeledButtonEntry,
    PasswordEntry,
    ENTRY_WIDGETS,
)
from .widgets.KeyPadWidgets import (
    BaseKeypad,
    DialerKeypad,
    KeypadButton,
    KEYPAD_WIDGETS,
)
from .widgets.ProgressbarWidgets import (
    LabeledProgressbar,
    LabeledMultiProgressbar,
    PROGRESSBAR_WIDGETS,
)
from .widgets.ScaleWidgets import LabeledScale, LabeledMultiScale, SCALE_WIDGETS
from .widgets.RadiobuttonWidgets import (
    LabeledRadiobutton,
    LabeledMultiRadiobutton,
    RADIOBUTTON_WIDGETS,
)
from .widgets.TextWidgets import ScrolledText, CopyBox, TEXT_WIDGETS
from .widgets.ConsoleWidgets import ConsoleWidget, CONSOLE_WIDGETS
from .widgets.ListBoxWidgets import ScrolledListBox, Table, LISTBOX_WIDGETS
from .widgets.TreeviewWidgets import TreeTable
from .widgets.ToplevelWidgets import (
    FocusedToplevel,
    NoticeWindow,
    YesNoCancelWindow,
    PromptWindow,
    PasswordWindow,
    ListWindow,
)
from .widgets.ToolTip import ToolTip
from .widgets.ResizableCanvas import ResizableCanvas
from .widgets.ScrolledCanvas import ScrolledCanvas, TiledCanvas, ExampleTile
from .widgets.SizegripWidgets import EasySizegrip
from .utils.color import (
    reduce,
    rgb_to_hex,
    rgba_to_hex,
    hex_to_rgb,
    hex_to_rgba,
    get_gradient,
    rgb_to_scalar,
    scalar_to_rgb,
    linear_gradient,
    get_rainbow,
    COLOR_FUNCTIONS,
)

from .utils.lorem_ipsum import get_lorem_paragraphs
from .utils.HTML_Generator import HTML_Generator
from .utils.TXT_Generator import TXT_Generator
from .utils.MD_Generator import MD_Generator
from .utils.utils import (
    check_if_module_installed,
    check_string_contains,
    dummy_function,
    get_friendly_time,
    get_installed_packages,
    get_unix_timestamp,
    get_unix_timestring,
    get_user_home_folder,
    open_folder_in_explorer,
    sort_dict_by_keys,
    timer_decorator,
)
from .utils.History import HistoryMixin
from .utils.scaling import enable_dpi_awareness
from .utils.ProfilesSystem import ProfilesSystem, UserProfile, get_profiles_folder, get_profiles_list, PROFILES_OBJECTS, PROFILES_FUNCTIONS
from .mega_widgets.chat import ConversationsTab
from .mega_widgets.notes import NotesTab
from .mega_widgets.profile_manager import ProfilesWindow
from .mega_widgets.timecard_maker import TimecardTab, TimecardMaker
from .mega_widgets.wattage_calculator import WattageTab, WattageCalculator
from .mega_widgets.shopping_list import ShoppingListTab, ShoppingList
from .mega_widgets.tictactoe import TicTacToeTab, TicTacToe

CANVAS_WIDGETS = [ResizableCanvas, ScrolledCanvas, TiledCanvas, ExampleTile]
TOPLEVEL_WIDGETS = [
    FocusedToplevel,
    NoticeWindow,
    YesNoCancelWindow,
    PromptWindow,
    PasswordWindow,
    ListWindow
]
MEGA_WIDGETS = [ConversationsTab, NotesTab]
UTILS = [
    check_if_module_installed,
    check_string_contains,
    dummy_function,
    get_friendly_time,
    get_installed_packages,
    get_unix_timestamp,
    get_unix_timestring,
    get_user_home_folder,
    open_folder_in_explorer,
    sort_dict_by_keys,
    timer_decorator,
]
FILE_GENERATORS = [
    HTML_Generator,
    TXT_Generator,
    MD_Generator,
]
MISC_WIDGETS = [ToolTip, EasySizegrip]
LOREM_IPSUM = [get_lorem_paragraphs]


if not check_if_module_installed("pillow"):
    PILLOW_AVAILABLE = False
    print("Pillow not detected, not importing pillow-only widgets")
else:
    PILLOW_AVAILABLE = True
    print("Pillow detected, importing pillow-only widgets")
    from .pillow_widgets.GifLoader import GifLoader, GifViewer
