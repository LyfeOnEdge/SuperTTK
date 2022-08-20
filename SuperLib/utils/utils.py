import os, sys, time, json, platform
import pkg_resources
from collections import OrderedDict

# # Check if a module is installed
# def check_if_module_installed(module_name: str):
#     """Checks is a module has been installed using pip. `Returns a Bool`"""
#     reqs = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
#     installed_packages = [r.decode().split("==")[0] for r in reqs.split()]
#     return module_name in installed_packages

def modify_filename(path, add):
    filename, ext = path.rsplit(".", 1)
    return filename+add+"."+ext

def check_string_contains(string:str, contains_list:tuple):
    """Returns `(True, char_index)` if any character from the list exists in the string otherwise returns `(False, None)`"""
    for c in contains_list:
        if c in string:
            return (True, string.index(c))
    return (False, None)

def get_installed_packages():
    """Get an alphabetized list of available packages. `Returns a List`"""
    return sorted([i.key for i in pkg_resources.working_set])

def check_if_module_installed(package):
    """Indicates if a packages is installed. `Returns a Boolean`"""
    return package in get_installed_packages()

def dummy_function(*args, **kwargs):
    """Dummy function that nicely prints out any passed args and kwargs. `Returns None`"""
    print(f"Dummy function ran with\n\targs:\n\t\t{args}\n\tkwargs:\n\t\t{kwargs}")


def timer_decorator(proc):
    """Decorator to add timing to a function"""
    def timed_func(*args, **kw):
        start = time.time_ns()
        res = proc(*args, **kw)
        stop = time.time_ns()
        print("%r  %2.2f ms" % (proc.__name__, (stop - start) / 1000000.0))
        return res

    return timed_func



def get_unix_timestamp():
    """Get a unix timestamp. `Returns a Float`"""
    return time.time_ns()


def get_unix_timestring():
    """Get a unix timestring. `Returns a String`"""
    return str(time.time_ns())


# Can be made more complex later to be friendly like "1 week ago"
def get_friendly_time(timestamp, mode="all"):
    """Gets a time string in one of several modes. Modes: `all, time, date, nice_date`. `Returns a String`"""
    if mode == "all":
        return time.strftime("%a %b %d %Y @ %I:%M%p", time.localtime(timestamp))
    elif mode == "time":
        return time.strftime("%I:%M%p", time.localtime(timestamp))
    elif mode == "date":
        return time.strftime("%b %d %Y", time.localtime(timestamp))
    elif mode == "nice_date":
        return time.strftime("%a %b %d %Y", time.localtime(timestamp))
    else:
        raise ValueError(f"Unsupported mode - {mode}")

def get_friendly_modified_time(path:str):
    """Get a readable modified date for a file"""
    return get_friendly_time(os.path.getmtime(path))

def get_user_home_folder():
    """Cross-platform function to get a user's home folder"""
    return os.path.expanduser("~")


def open_folder_in_explorer(path):
    """Cross-platform way to open a folder in the default file manager for a system"""
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def sort_dict_by_keys(source: dict, reverse: bool = False):
    """Sorts a dictionary by its keys"""
    item = reversed(d.items()) if reverse else d.items()
    return OrderedDict(sorted(items, key=lambda k: k[0]))


class PyScriptRunner:
    """Runs a python script as a subprocess"""

    def __init__(self, script_path, print_function=print, cwd=os.getcwd()):
        self.script_path = script_path
        self.print_function = print_function
        self.cwd = cwd
        self.running = False

    def run(self, arguments):
        self.running = True
        wd = os.getcwd()
        os.chdir(self.cwd)
        args = [sys.executable, "-u", self.script_path]
        args.extend(arguments)
        try:
            p = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
            )
            with p.stdout:
                for line in iter(p.stdout.readline, b""):
                    self.do_print_function(line)
            p.wait()
        except Exception as e:
            self.do_print_function("ERROR - {e}")
        finally:
            os.chdir(wd)
            self.running = False

    def do_print_function(self, string):
        if self.print_function:
            self.print_function(string)
            sys.stdout.flush()

# Public domain code to convert SI size in to be friendly, does bytes by default
def format_SI(num, suffix="B"):
    divider = 1024  # 1000 for MiB
    for unit in ["", "k", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
