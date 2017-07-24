import flickrapi

import os, sys
import argparse
from datetime import date
from logging import getLogger
log = getLogger(__name__)

API_KEY = '23005d9cf8cc185c1c2d17152d03d98b'

SIZES = ('Square', 'Large Square', 'Thumbnail', 'Small', 'Small 320',
         'Medium', 'Medium 640', 'Medium 800', 'Large', 'Large 1600',
         'Large 2048', 'Original')

flickr = flickrapi.FlickrAPI(API_KEY, '')
HOME = os.environ.get('HOME')
USER = os.environ.get('USER')

def parse_opts(opts):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dump', '-d', dest='dump', nargs=1,
                        help= "Dump file for used photo ids.",
                        type=str, default=os.path.join(HOME, '.flickpaper.dump'),
    )
    parser.add_argument('--image', '-i', dest='image', nargs=1,
                        help= "Where to store the downloaded image.",
                        type=str, default=get_default_image_path(),
    )
    parser.add_argument('--log', '-l', dest='log', nargs=1,
                        help= "Path to log file.",
                        type=str, default=None,
    )
    parser.add_argument('--per-page', '-p', dest='per_page', nargs=1,
                        help= "Number of interesting photos per page in flickr api call.",
                        type=int, default=100,
    )
    parser.add_argument('--date', dest='date', nargs=1,
                        help= "A specific date, formatted as YYYY-MM-DD, to return interesting photos for. Default: null (most recent)",
                        type=date, default=None,
    )
    parser.add_argument('--page', dest='page', nargs=1,
                        help= "The page of results to return. Default: #{options[:page]}",
                        type=int, default=1,
    )
    parser.add_argument('--size', '-s', dest='size', nargs=1,
                        help= "Minimum acceptable image size. Default: #{options[:size]}",
                        type=str, default='Large 2048',
    )
    parser.add_argument('--verbose', '-v', dest='verbose',
                        help= "Be verbose.", action='store_const',
                        const=True, default=False,
    )
    parser.add_argument('--sizes', dest='sizes',
                        help= "Print sizes and exit.", action='store_const',
                        const=True, default=False,
    )
    parser.add_argument('--version', dest='version',
                        help= "Print version and exit.", action='store_const',
                        const=True, default=False,
    )

    res = parser.parse_args(opts)
    if res.sizes:
        print(', '.join(SIZES))
        sys.exit(0)
    elif res.version:
        print('0.1')
        sys.exit(0)
    else:
        return res

def save_file(url, dst):
    import wget
    wget.download(url, dst)

def window_manager():
    CURR_DESK = os.environ.get('XDG_CURRENT_DESKTOP')
    DATA_DIRS = os.environ.get('XDG_DATA_DIRS')
    if CURR_DESK:
        desktop = CURR_DESK.lower()
    else:
        exclude = ('usr', 'local', 'share')
        v = DATA_DIRS.lower().split('/:')
        if len(v) == 1:
            desktop = v[0].lower()
    return desktop

def set_wallpaper():
    _os = sys.platform
    if _os=='windows':
        pass
    elif _os=='darwin':
        set_wallpaper_macosx(path)
    elif _os in ('linux', 'freebsd'):
        set_wallpaper_linux(path)
    else:
        pass

def set_wallpaper_macosx(path):
    pass

def set_wallpaper_linux(path):
    wm = window_manager()
    if wm == 'gnome':
        set_wallpaper_gnome(path)
    elif wm == 'kde':
        set_wallpaper_kde(path)
    else:
        set_wallpaper_feh(path)

def set_wallpaper_gnome(path):
    bash = """
        if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
          # if not found, launch a new one
          eval `#{dbus_launch} --sh-syntax`
        fi

        gsettings set org.gnome.desktop.background picture-uri "file://{path}"
    """.format(path=path)

def set_wallpaper_feh():
    os.system('feh --bg-fill {}'.format(path))

def set_wallpaper_kde():
    pass

def get_default_image_path():
    _os = sys.platform
    if _os=='windows':
        return None
    elif _os=='darwin':
        home_tmp = os.path.join(HOME, 'tmp')
        if os.path.isdir(home_tmp):
            return os.path.join(home_tmp, 'flickpaper-{}.jpg'.format(USER))
        else:
            return os.path.join('/tmp', 'flickpaper-{}.jpg'.format(USER))
    elif _os in ('linux', 'freebsd'):
        return os.path.join(HOME, '.flickpaper.jpg') 


if __name__=='__main__':
    print(parse_opts(sys.argv[1:]))
