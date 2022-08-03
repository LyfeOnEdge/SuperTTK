import os, re
if os.name == "nt":
    from ctypes import windll, pointer, wintypes
    
def Get_HWND_DPI(window_handle, scale):
    #To detect high DPI displays and avoid need to set Windows compatibility flags
    if os.name == "nt":
        try:
            windll.shcore.SetProcessDpiAwareness(scale)
        except Exception:
            pass  # this will fail on Windows Server and maybe early Windows
        DPI100pc = 96  # DPI 96 is 100% scaling
        DPI_type = 0  # MDT_EFFECTIVE_DPI = 0, MDT_ANGULAR_DPI = 1, MDT_RAW_DPI = 2
        winH = wintypes.HWND(window_handle)
        monitorhandle = windll.user32.MonitorFromWindow(winH, wintypes.DWORD(2))  # MONITOR_DEFAULTTONEAREST = 2
        X = wintypes.UINT()
        Y = wintypes.UINT()
        try:
            windll.shcore.GetDpiForMonitor(monitorhandle, DPI_type, pointer(X), pointer(Y))
            return X.value, Y.value, (X.value + Y.value) / (2 * DPI100pc)
        except Exception:
            return 96, 96, 1  # Assume standard Windows DPI & scaling
    else:
        return None, None, 1  # What to do for other OSs?

def TkGeometryScale(s, cvtfunc):
    patt = r"(?P<W>\d+)x(?P<H>\d+)\+(?P<X>\d+)\+(?P<Y>\d+)"  # format "WxH+X+Y"
    R = re.compile(patt).search(s)
    G = str(cvtfunc(R.group("W"))) + "x"
    G += str(cvtfunc(R.group("H"))) + "+"
    G += str(cvtfunc(R.group("X"))) + "+"
    G += str(cvtfunc(R.group("Y")))
    return G

def enable_dpi_awareness(app, scale):
    """Based on https://github.com/not-dev/high-dpi-tkinter/blob/master/src/hdpitkinter/high_dpi_tkinter.py MIT License"""
    app.window.DPI_X, app.window.DPI_Y, app.window.DPI_scaling = Get_HWND_DPI(app.window.winfo_id(), scale)
    app.window.TkScale = lambda v: int(float(v) * app.window.DPI_scaling)
    app.window.TkGeometryScale = lambda s: TkGeometryScale(s, app.window.TkScale)
