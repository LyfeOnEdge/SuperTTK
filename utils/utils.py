import os, sys, subprocess, webbrowser

def run_cl(commands: list):
	subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def open_link(link: str):
	print(f'Opening {link} in default web browser')
	webbrowser.open_new_tab(link)

def check_module_installed_status(module_name):
	reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
	installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
	return module_name in installed_packages

def get_local_appdata_folder(): return os.path.expandvars('%LOCALAPPDATA%')

def open_folder_in_window(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def sorted_dict_by_key(source:dict,reverse:bool=False):
	item = reversed(d.items()) if reverse else d.items() 
	return OrderedDict(sorted(items, key=lambda k: k[0]))