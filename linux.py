from os import environ, system

def window_manager():
    # Should work for most DE (gnome, kde, xfce, i3, openbox)
    SESSION_DESKTOP = environ.get('XDG_SESSION_DESKTOP')
    DESKTOP_SESSION = environ.get('DESKTOP_SESSION')
    desktop = SESSION_DESKTOP or DESKTOP_SESSION
    return desktop

def set_wallpaper_linux(path):
    wm = window_manager()
    if wm == 'gnome':
        set_wallpaper_gnome(path)
    elif wm == 'kde':
        set_wallpaper_kde(path)
    elif wm == 'xfce':
        set_wallpaper_xfce(path)
    elif wm == 'lxde':
        set_wallpaper_lxde(path)
    elif wm in ('i3', 'openbox'):
        set_wallpaper_feh(path)
    else:
        print("Unsupported window manager: {}".format(wm))

def set_wallpaper_gnome(path):
    try:
        from gi.repository import Gio
        print("Using gsettings api")
        settings = Gio.Settings.new("org.gnome.desktop.background")
        settings.set_string("picture-uri", "file://" + path)
        settings.apply()
    except ImportError:
        print("Using gsettings cmd")
        bash = """
        gsettings set org.gnome.desktop.background picture-uri "file://{}"
        """.format(path)
        system(bash)

def set_wallpaper_xfce(path):
    bash = """
    xfconf-query -c xfce4-desktop -p \
        /backdrop/screen0/monitor0/workspace0/last-image -s {}
    """.format(path)
    system(bash)

def set_wallpaper_feh(path):
    bash = "feh --bg-fill {}".format(path)
    system(bash)

def set_wallpaper_kde(path):
    # It's PlasmaScript BTW
    bash = """
    dbus-send --session --dest=org.kde.plasmashell --type=method_call \
	/PlasmaShell org.kde.PlasmaShell.evaluateScript 'string:
	    var Desktops = desktops();
	    for (i=0;i<Desktops.length;i++) {
		    d = Desktops[i];
		    d.wallpaperPlugin = "org.kde.image";
		    d.currentConfigGroup = Array("Wallpaper",
						"org.kde.image",
						"General");
		    d.writeConfig("Image", "file://{}");
	    }'
    """.format(path)
    system(bash)

def set_wallpaper_lxde(path):
    # It's funny that it's so easy
    bash = "pcmanfm -w {}".format(path)
    system(bash)

