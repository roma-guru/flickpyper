from os import system

def set_wallpaper_macosx(path):
    from appscript import app, mactypes
    app('Finder').desktop_picture.set(mactypes.File(path))

def set_wallpaper_windows(path):
    # I thought that will be harder
    import ctypes
    SPI = 20
    SPIF = 2
    # Should support not only bmp but jpg
    # TODO: problems with nonascii
    ctypes.windll.user32.SystemParametersInfoA(
        SPI, 0, path.encode('us-ascii'), SPIF)

