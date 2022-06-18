import json

json_data = {
    "application": "Test Application",
    "version": "0.0",
    "width": 400,
    "height": 400,
    "minwidth": 60,
    "minheight": 60,
    "resizable_width": True,
    "resizable_height": True,
    "start_maximized": False,
    "enable_maximized": True,
    "start_fullscreen": False,
    "enable_fullscreen": True,
    "enable_themes_menu": True,
    "scaling": 2,
    "icon": None,  # Set to icon path relative to script file
}

print(json.dumps(json_data, indent=4))


# todo: make this a proper script with args etc
