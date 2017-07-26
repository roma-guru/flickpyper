from flickrapi import FlickrAPI, FlickrError

from os import environ, path
import sys
import argparse
from datetime import date
from logging import getLogger
log = getLogger(__name__)

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
    wget.download(url, dst)

def window_manager():
    CURR_DESK = environ.get('XDG_CURRENT_DESKTOP')
    DATA_DIRS = environ.get('XDG_DATA_DIRS')
    # TODO: $XDG_SESSION_DESKTOP, $XDG_MENU_PREFIX, $DESKTOP_SESSION
    # TODO: test other wms
    if CURR_DESK:
        desktop = CURR_DESK.lower()
    else:
        exclude = ('usr', 'local', 'share')
        v = DATA_DIRS.lower().split('/:')
        if len(v) == 1:
            desktop = v[0].lower()
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

def set_wallpaper():
    _os = os()
    if _os=='windows':
        pass
    elif _os=='macosx':
        set_wallpaper_macosx(path)
    elif _os in ('linux', 'unix'):
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
    # TODO: can we do better? There must be python bindings!
    bash = """
        if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
          # if not found, launch a new one
          eval `dbus-launch --sh-syntax`
        fi

        gsettings set org.gnome.desktop.background picture-uri "file://{path}"
    """.format(path=path)

def set_wallpaper_feh():
    os.system('feh --bg-fill {}'.format(path))

def set_wallpaper_kde():
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
    pass

def put_ids(file, ids):
    pass

def run():
    options = parse_opts(sys.argv[1:])

    size_idx = SIZES.index(options.size)
    if not size_idx or size_idx < 0:
        log.error("Invalid size argument: #{options[:size]}.\nPlease select from: #{SIZES.join(', ')}.")
        sys.exit(1)

    opts = {k:v for (k,v) in d.items() if k in ('page','per_page','date') and v}
    log.info("Getting interesting list: #{opts.inspect}")
    try:
        list = flickr.interestingness.getList()
    except FlickrError as e:
        log.error("Flickr API error: {}".format(e.code))
        sys.exit(1)

    ids = get_ids(options.dump)
    list = [i for i in list if i not in ids]

    idx = None
    url = None

    log.info("Selecting large photo")
    for i in range(len(list)):
        try:
            size = flickr.photos.getSizes(photo_id=list[i]['id'])
        except FlickrError as e:
            log.error("Flickr API error: #{e.message}")
            sys.exit(1)
        def detect(s):
            my_size_idx = SIZES.index(s['label'])
            return my_size_idx and my_size_idx >= size_idx
        my_size = filter(detect, size)[0]
        if my_size:
            idx = i
            url = my_size['source']
            break

    if idx:
        my_photo = list[idx]

        save_file(url, options.image)
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
