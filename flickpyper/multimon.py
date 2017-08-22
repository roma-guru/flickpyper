import sys

def get_screen_count_gnome():
    import gi
    gi.require_version('Gdk','3.0')
    from gi.repository import Gdk
    d = Gdk.Display()
    return d.get_n_monitors()

def get_screen_count_x():
    try:
        # Try python-xlib
        from Xlib import X, display
    except ImportError:
        # Try xrandr app
        bash = 'xrandr -q | grep Screen | wc -l'
        return int(os.popen(bash).read())
    d = display.Display()
    return d.screen_count()

def get_screen_count_win32():
    import win32api
    return len(win32api.EnumDisplayMonitors())
