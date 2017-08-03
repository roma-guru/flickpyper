from os import system

def set_wallpaper_macosx(path):
    try:
        # Nicer way
        from appscript import app, mactypes
        app('Finder').desktop_picture.set(mactypes.File(path))
    except ImportError:
        # Uglier way
        bash = """
        osascript -e 'tell application "Finder" to set desktop picture to POSIX file "{}"
        """.format(path)
        system(bash)

def set_wallpaper_windows(path):
    # I thought that will be harder
    import ctypes
    SPI = 20
    SPIF = 2
    # Should support not only bmp but jpg
    ctypes.windll.user32.SystemParametersInfoW(
        SPI, 0, path.encode('utf16'), SPIF)

