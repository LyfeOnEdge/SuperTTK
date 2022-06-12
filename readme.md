See SuperTTK.py for arguments / example usages 

### Available widgets (import from SuperTTK.py)
	LabeledCheckbutton
	LabeledMultiCheckbutton
	LabeledCombobox
	LabeledMultiCombobox
	LabeledOptionMenu
	LabeledMultiOptionMenu
	LabeledEntry
	LabeledMultiEntry
	LabeledProgressbar
	LabeledMultiProgressbar
	LabeledScale
	LabeledMultiScale
	LabeledRadiobutton
	LabeledMultiRadiobutton
	ScrolledText

### Labeled Widgets:
	
	Widgets wrapped in a frame with a label placed to the left and the widget packed to the top

	Consistent init args for base labeled widgets (does not apply to multi-widgets)
		default (either a default values or index of the default in passed options)

	Consistent Methods:
		.enable()
		.disable()
		.set()
		.get()
		.clear() #Resets to the default
		.link() #Only available on some display widgets like LabeledProgressbars, links to an input widget

### Multi Widgets:
	Labeled Widgets with labeled sub-widgets of a given type



### Credits:

Sun-Valley-ttk-theme: [MIT] https://github.com/rdbende/Sun-Valley-ttk-theme