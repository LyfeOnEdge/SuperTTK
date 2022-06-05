import json

json_data = {
	"application" : "Test Application",
	"version": "0.0",
	"width" : 600,
	"height" : 600,
	"minwidth" : 600,
	"minheight" : 600,
	"resizable_width" : True,
	"resizable_height" : True,
	"start_maximized" : False,
	"scaling" : 2,
}

print(json.dumps(json_data, indent=4))


#todo: make this a proper script with args etc