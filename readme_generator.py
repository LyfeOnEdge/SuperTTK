from SuperLib import (
    MD_Generator,
    ENTRY_WIDGETS,
    CHECKBUTTON_WIDGETS,
    COMBOBOX_WIDGETS,
    CONSOLE_WIDGETS,
    KEYPAD_WIDGETS,
    LISTBOX_WIDGETS,
    OPTIONMENU_WIDGETS,
    PROGRESSBAR_WIDGETS,
    RADIOBUTTON_WIDGETS,
    SCALE_WIDGETS,
    TABS,
    HistoryMixin,
    COLOR_FUNCTIONS,
    CORE_FUNCTIONS,
    CORE_OBJECTS,
    CANVAS_WIDGETS,
    TOPLEVEL_WIDGETS,
    NotesTab,
    ConversationsTab,
    UTILS,
    FILE_GENERATORS,
    TEXT_WIDGETS,
    MISC_WIDGETS,
    PROFILES_OBJECTS,
    PROFILES_FUNCTIONS,
) 
from inspect import getfullargspec, signature
import json

IGNORED_METHODS = ["addtag","addtag_above","addtag_all","addtag_below","addtag_closest","addtag_enclosed","addtag_overlapping","addtag_withtag","after","after_cancel","after_idle","anchor","aspect","attributes","bbox","bell","bind","bind_all","bind_class","bindtags","canvasx","canvasy","cget","client","clipboard_append","clipboard_clear","clipboard_get","colormapwindows","columnconfigure","command","compare","config","configure","coords","count","current","dchars","debug","deiconify","delete","deletecommand","dlineinfo","dtag","dump","edit","edit_modified","edit_redo","edit_reset","edit_separator","edit_und","event_add","event_delete","event_generate","event_info","find","find_above","find_all","find_below","find_closest","find_enclosed","find_overlapping","find_withtag","focus","focus_displayof","focus_force","focus_get","focus_lastfor","focus_set","focusmodel","forget","frame","geometry","getboolean","getdouble","getint","gettags","getvar","grab_current","grab_release","grab_set","grab_set_global","grab_status","grid","grid_anchor","grid_bbox","grid_columnconfigure","grid_configure","grid_forget","grid_info","grid_location","grid_propagate","grid_remove","grid_rowconfigure","grid_size","grid_slaves","group","iconbitmap","iconify""iconmask","iconname","iconphoto","iconposition","iconwindow","icursor","identify","image_cget","image_configure","image_create","image_names","image_types","index","info","insert","instate","invoke","itemcget","itemconfig","itemconfigure","keys","lift","location","lower","mainloop","manage","mark_gravity","mark_names","mark_next","mark_previous","mark_set","mark_unset","maxsize","minsize","move","moveto","moveto","nametowidget","nearest","option_add","option_clear","option_get","option_readfile","overrideredirect","pack","pack_configure","pack_forget","pack_info","pack_propagate","pack_slaves","peer_create","peer_names","place","place_configure","place_forget","place_info","place_slaves","positionfrom","postscript","propagate","protocol","quit","register","replace","resizable","rowconfigure","scale","scan_dragto","scan_mark","search","see","select_adjust","select_anchor","select_clear","select_from","select_includes","select_item","select_present","select_range","select_set","select_to","selection_adjust","selection_anchor","selection_clear","selection_clear","selection_from","selection_get","selection_handle","selection_includes","selection_own","selection_own_get","selection_present","selection_range","selection_set","selection_to","send","set_cursor","set_label_text","setvar","size","sizefrom","slaves","state","tag_add","tag_bind","tag_bing","tag_cget","tag_config","tag_configure","tag_delete","tag_lower","tag_names","tag_nextrange","tag_prevrange","tag_raise","tag_ranges","tag_remove","tag_unbind","title","tk_bisque","tk_focusFollowsMouse","tk_focusNext","tk_focusPrev","tk_setPalette","tk_strictMotif","tkraise","transient","type","unbind","unbind_all","unbind_class","update","update_idletasks","validate","wait_variable","wait_visibility","wait_window","waitvar","window_cget","window_config","window_configure","window_names","winfo_atom","winfo_atomname","winfo_cells","winfo_children","winfo_class","winfo_colormapfull","winfo_containing","winfo_depth","winfo_exists","winfo_fpixels","winfo_geometry","winfo_height","winfo_id","winfo_interps","winfo_ismapped","winfo_manager","winfo_name","winfo_parent","winfo_pathname","winfo_pixels","winfo_pointerx","winfo_pointerxy","winfo_pointery","winfo_reqheight","winfo_reqwidth","winfo_rgb","winfo_rootx","winfo_rooty","winfo_screen","winfo_screencells","winfo_screendepth","winfo_screenheight","winfo_screenmmheight","winfo_screenmmwidth","winfo_screenvisual","winfo_screenwidth","winfo_server","winfo_toplevel","winfo_viewable","winfo_visual","winfo_visualid","winfo_visualsavailable","winfo_vrootheight","winfo_vrootwidth","winfo_vrootx","winfo_vrooty","winfo_width","winfo_x","winfo_y","withdraw","wm_aspect","wm_attributes","wm_client","wm_colormapwindows","wm_command","wm_deiconify","wm_focusmode","wm_focusmodel","wm_forget","wm_frame","wm_geometry","wm_grid","wm_group","wm_iconbitmap","wm_iconify","wm_iconmask","wm_iconname","wm_iconphoto","wm_iconposition","wm_iconwindow","wm_manage","wm_maxsize","wm_minsize","wm_overrideredirect","wm_positionfrom","wm_protocol","wm_resizable","wm_sizefrom","wm_state","wm_title","wm_transient","wm_withdraw","xview","xview_moveto","xview_scroll","yview","yview_moveto","yview_pickplace","yview_scroll"]

slogan = "Themes don't have to be hard."

about_text = """SuperTTK exists because I got tired of rewriting the same code over \
and over for simple projects. The goal is to provide a variety of meta widgets with \
consistent get/set/enable/disable/destroy methods and mega-widgets that make ttk \
development easier and faster. Features include built-in theme support, a score of \
labeled and multi-widgets, tools for easy form building, a sample application \
demonstrating many of SuperTTK's features, a configuration file system, and much more. \
![Lines of code](https://img.shields.io/tokei/lines/github/LyfeOnEdge/SuperTTK)"""

requirements_text = ""

ini_conf = """+--------------------+-------------------------------------------+
|        Key         |                   Value                   |
+--------------------+-------------------------------------------+
| application        | Application Name (String)                 |
| version            | Application Version (String)              |
| icon               | Application Icon Path (String)            |
| width              | Startup Window Width (Int)                |
| height             | Startup Window Height (Int)               |
| minwidth           | Window Minimum Width (Int)                |
| minheight          | Window Minimum Height (Int)               |
| scaling            | Window Scaling (Float)                    |
| scale_minsize      | Scale application Minimum Size (Boolean)  |
| scale_startsize    | Scale application Start Size (Boolean)    |
| resizable_width    | Enable Window Width Resizing (Boolean)    |
| resizable_height   | Enable Window Height Resizing (Boolean)   |
| start_maximized    | Start Window Maximized (Boolean)          |
| enable_maximized   | Enable Window Maximized (Boolean)         |
| start_fullscreen   | Start Window in Fullscreen mode (Boolean) |
| enable_fullscreen  | Enable Window Fullscreen option (Boolean) |
| enable_themes_menu | Enable Themes Dropdown (Boolean)          |
| movable_tabs       | Enable Moveable Notebook Tabs (Boolean)   |
| enable_users       | Enable a User Profiles System             |
+--------------------+-------------------------------------------+"""

gen = MD_Generator(title="SuperTTK", footnote_heading_level=3)

def handle_class_list(widgets):
    gen.increase_toc_depth()
    for w in widgets:
        gen.add_heading_3(w.__module__ + "." + w.__name__, end="")
        gen.add_toc(w.__name__)
        gen.quote_depth += 1
        if w.__doc__:# Add docstring 
            gen.add_paragraph(f"**{w.__doc__}**", end=f"\n{gen.get_prefix()}\n")
            # gen.add_heading_5(w.__doc__, line="\n")
        if hasattr(w, "__desc__"): #Only print desc if it isn't inherited
            desc_inherited = False
            for b in w.__bases__:
                if hasattr(b, "__desc__"):
                    if b.__desc__ == w.__desc__:
                        desc_inherited = True
                        break
            if not desc_inherited:
                gen.add_paragraph(w.__desc__,end="\n")

        classstring = f"class {w.__name__}("
        if len(w.__bases__) == 1:
            b = w.__bases__[0]
            classstring += b.__module__ + "." + b.__name__
        else:
            last = len(w.__bases__) - 1
            i = 0
            for b in w.__bases__:
                classstring += b.__module__ + "." + b.__name__
                if not i == last:
                    classstring += ", "
                i += 1
        classstring += "):\n"
        sig = str(signature(w)).strip('"')
        sig = sig[:1] + "self, " + sig[1:]
        classstring = classstring + "\tdef __init__" + sig + ":\n\t\t...\n"
        methods = [m for m in dir(w) if (m.startswith('_') is False) and callable(getattr(w, m)) and (not m in IGNORED_METHODS)]
        if methods:
            for m in methods:
                meth = getattr(w, m)
                val = "..."
                if hasattr(meth, "__doc__"):
                    if meth.__doc__:
                        val = f'"""{meth.__doc__}"""'
                classstring += f"\tdef {m}{str(signature(meth))}:\n\t\t{val}\n"
            
        gen.add_code_block(classstring.replace("\n","\n"+gen.get_prefix()), lang="py")
        gen.quote_depth -= 1
    gen.decrease_toc_depth()
               
def handle_function_list(functions):
    gen.increase_toc_depth()
    for f in functions:
        gen.add_heading_3(f.__module__ + "." + f.__name__, end="")
        gen.add_toc(f.__name__)
        gen.quote_depth += 1
        gen.add_paragraph(f"**{f.__doc__}**", end=f"\n{gen.get_prefix()}\n")
        name = f.__module__ + "." + f.__name__
        funcstring = f"def {name}{str(signature(f))}:\n{gen.get_prefix()}\t..."
        gen.add_code_block(funcstring, lang="py")
        gen.quote_depth -= 1
    gen.decrease_toc_depth()

gen.set_slogan(slogan)
gen.add_heading_1("About", add_toc=True)
gen.add_paragraph(about_text)
gen.add_heading_1("Requirements", add_toc=True)
gen.add_paragraph(requirements_text)
gen.add_heading_1("Configuring ini.json",add_toc=True)
gen.add_code_block(ini_conf)
gen.add_heading_1("SuperLib.widgets",add_toc=True)
gen.increase_toc_depth()
gen.add_heading_2("Core Functions",add_toc=True)
handle_function_list(CORE_FUNCTIONS)
gen.add_heading_2("Core Widgets",add_toc=True)
handle_class_list(CORE_OBJECTS)
gen.add_heading_2("Tabs",add_toc=True)
handle_class_list(TABS)
gen.add_heading_2("Canvas Widgets",add_toc=True)
handle_class_list(CANVAS_WIDGETS)
gen.add_heading_2("Checkbutton Widgets",add_toc=True)
handle_class_list(CHECKBUTTON_WIDGETS)
gen.add_heading_2("Combobox Widgets",add_toc=True)
handle_class_list(COMBOBOX_WIDGETS)
gen.add_heading_2("Console Widgets",add_toc=True)
handle_class_list(CONSOLE_WIDGETS)
gen.add_heading_2("Entry Widgets",add_toc=True)
handle_class_list(ENTRY_WIDGETS)
gen.add_heading_2("KeyPad Widgets",add_toc=True)
handle_class_list(KEYPAD_WIDGETS)
gen.add_heading_2("ListBox Widgets",add_toc=True)
handle_class_list(LISTBOX_WIDGETS)
gen.add_heading_2("OptionMenu Widgets",add_toc=True)
handle_class_list(OPTIONMENU_WIDGETS)
gen.add_heading_2("ProgressBar Widgets",add_toc=True)
handle_class_list(PROGRESSBAR_WIDGETS)
gen.add_heading_2("Radiobutton Widgets",add_toc=True)
handle_class_list(RADIOBUTTON_WIDGETS)
gen.add_heading_2("Scale Widgets",add_toc=True)
handle_class_list(SCALE_WIDGETS)
gen.add_heading_2("Text Widgets", add_toc=True)
handle_class_list(TEXT_WIDGETS)
gen.add_heading_2("Toplevel Widgets",add_toc=True)
handle_class_list(TOPLEVEL_WIDGETS)
gen.add_heading_2("Misc Widgets",add_toc=True)
handle_class_list(MISC_WIDGETS)
gen.decrease_toc_depth()
gen.add_heading_1("SuperLib.utils",add_toc=True)
gen.increase_toc_depth()
gen.add_heading_2("Utils", add_toc=True)
handle_function_list(UTILS)
gen.add_heading_2("File Generators",add_toc=True)
handle_class_list(FILE_GENERATORS)
gen.add_heading_2("History Mixin",add_toc=True)
handle_class_list([HistoryMixin])
gen.add_heading_2("Color Functions",add_toc=True)
handle_function_list(COLOR_FUNCTIONS)
gen.decrease_toc_depth()
gen.add_heading_1("SuperLib.mega_widgets",add_toc=True)
gen.increase_toc_depth()
gen.add_heading_2("Notes MegaWidget",add_toc=True)
handle_class_list([NotesTab])
gen.add_heading_2("Conversation MegaWidget",add_toc=True)
handle_class_list([ConversationsTab])

gen.add_heading_2("Profile Management",add_toc=True)
handle_class_list(PROFILES_OBJECTS)
handle_function_list(PROFILES_FUNCTIONS)

gen.decrease_toc_depth()
out = gen.assemble()

print(out)
with open("readme.md", "w+") as f:
    f.write(out)     
import os
os.startfile("readme.md")