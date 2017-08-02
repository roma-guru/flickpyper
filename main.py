from flickrapi import FlickrAPI, FlickrError

from os import environ, path, remove, system
import sys, pickle
import argparse
from datetime import date
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

API_KEY = '23005d9cf8cc185c1c2d17152d03d98b'

VERSION = '0.1'
SIZES = ('Square', 'Large Square', 'Thumbnail', 'Small', 'Small 320',
         'Medium', 'Medium 640', 'Medium 800', 'Large', 'Large 1600',
         'Large 2048', 'Original')

HOME = environ.get('HOME')
USER = environ.get('USER')

flickr = FlickrAPI(API_KEY, '', format='parsed-json')

def parse_opts(opts):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dump', '-d', dest='dump', nargs=1,
                        help= "Dump file for used photo ids.",
                        type=str, default=path.join(HOME, '.flickpaper.dump'),
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
        print(VERSION)
        sys.exit(0)
    else:
        return res

def save_file(url, dst):
    import wget
    remove(dst)
    wget.download(url, dst)

def window_manager():
    # Should work for most DE (gnome, kde, xfce, i3, openbox)
    SESSION_DESKTOP = environ.get('XDG_SESSION_DESKTOP')
    DESKTOP_SESSION = environ.get('DESKTOP_SESSION')
    desktop = SESSION_DESKTOP or DESKTOP_SESSION
    return desktop

def os():
    host_os = sys.platform
    if host_os in ('cygwin', 'windows'):
        return 'windows'
    elif host_os in ('darwin',):
        return 'macosx'
    elif host_os in ('linux',):
        return 'linux'
    elif host_os in ('solaris', 'bsd'):
        return 'unix'
    else:
        return 'unknown'

def set_wallpaper(path):
    _os = os()
    if _os=='windows':
        log.debug("Windows")
        pass
    elif _os=='macosx':
        log.debug("Mac")
        set_wallpaper_macosx(path)
    elif _os in ('linux', 'unix'):
        log.debug("Linux")
        set_wallpaper_linux(path)
    else:
        log.error("Unsupported machine")
        return False
    return True

def set_wallpaper_macosx(path):
    # Not tested
    bash = """
    osascript -e 'tell application "Finder" to set desktop picture to POSIX file "{}"
    """.format(path)
    system(bash)

def set_wallpaper_linux(path):
    wm = window_manager()
    if wm == 'gnome':
        set_wallpaper_gnome(path)
    elif wm == 'kde':
        set_wallpaper_kde(path)
    elif wm == 'xfce':
        set_wallpaper_xfce(path)
    elif wm in ('i3', 'openbox'):
        set_wallpaper_feh(path)
    else:
        print("Unsupported window manager: {}".format(wm)

def set_wallpaper_gnome(path):
    from gi.repository import Gio
    settings = Gio.Settings.new("org.gnome.desktop.background")
    settings.set_string("picture-uri", "file://" + path)
    settings.apply()

def set_wallpaper_xfce(path):
    bash = """bash -c "
    xfconf-query -c xfce4-desktop -p \
        /backdrop/screen0/monitor0/workspace0/last-image -s {}"
    """.format(path)
    system(bash)

def set_wallpaper_feh(path):
    system('feh --bg-fill {}'.format(path))

def set_wallpaper_kde(path):
    pass

def get_default_image_path():
    _os = os()
    if _os=='windows':
        return None
    elif _os=='macosx':
        home_tmp = path.join(HOME, 'tmp')
        if path.isdir(home_tmp):
            return path.join(home_tmp, 'flickpaper-{}.jpg'.format(USER))
        else:
            return path.join('/tmp', 'flickpaper-{}.jpg'.format(USER))
    elif _os in ('linux', 'unix'):
        return path.join(HOME, '.flickpaper.jpg')

def get_ids(file):
    if path.isfile(file):
        with open(file, 'rb') as f:
            return pickle.load(f)
    else:
        return []

def put_ids(file, ids):
    with open(file, 'wb') as f:
        pickle.dump(ids, f)

def run():
    options = parse_opts(sys.argv[1:])
    log.debug(f"options = {options}")

    size_idx = SIZES.index(options.size)
    log.debug(f"size_idx = {size_idx}")
    if not size_idx or size_idx < 0:
        log.error(f"Invalid size argument: {options['size']}.\
                  \nPlease select from: {', '.join(SIZES)}.")
        sys.exit(1)

    opts = {k:v for (k,v) in vars(options).items() if k in ('page','per_page','date') and v}
    log.info(f"Getting interesting list: {opts}")
    try:
        list = flickr.interestingness.getList(**opts)['photos']['photo']
    except FlickrError as e:
        log.error(f"Flickr API error: {e.code}")
        sys.exit(1)

    log.debug(f"list = {list}")
    try:
        ids = get_ids(options.dump)
    except:
        # That's ok, file from Ruby version
        ids = []
    log.debug("ids = {ids}")
    list = [i for i in list if i not in ids]

    idx = None
    url = None

    log.info("Selecting large photo")
    for i in range(len(list)):
        try:
            size = flickr.photos.getSizes(photo_id=list[i]['id'])['sizes']['size']
        except FlickrError as e:
            log.error(f"Flickr API error: {e.code}")
            sys.exit(1)
        log.debug(f"size = {size}")
        def detect(s):
            my_size_idx = SIZES.index(s['label'])
            return my_size_idx and my_size_idx >= size_idx
        my_size = next(filter(detect, size))
        log.debug(f"my_size = {my_size}")
        if my_size is not None:
            idx = i
            url = my_size['source']
            log.debug(f"url = {url}")
            break

    if idx is not None:
        my_photo = list[idx]
        log.debug(f"my_photo = {my_photo}")

        log.info("Saving picture")
        save_file(url, options.image)
        log.info("Setting wallpaper")
        result = set_wallpaper(options.image)
        if result:
            log.info("Set photo #{my_photo['id']} as wallpaper")
            ids.append(my_photo['id'])
            put_ids(options.dump, ids)
        else:
            log.error("Unable to set photo #{my_photo['id']} as wallpaper")
    else:
        log.error("Unable to find photo for wallpaper")

if __name__=='__main__':
    run()
