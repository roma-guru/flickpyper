from flickrapi import FlickrAPI, FlickrError

from os import environ, path, remove, system
import sys, pickle
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

API_KEY = '23005d9cf8cc185c1c2d17152d03d98b'

VERSION = '0.1'
SIZES = ('Square', 'Large Square', 'Thumbnail', 'Small', 'Small 320',
         'Medium', 'Medium 640', 'Medium 800', 'Large', 'Large 1600',
         'Large 2048', 'Original')

flickr = FlickrAPI(API_KEY, '', format='parsed-json')

from .options import parse_opts
from .common import os, save_file
from .winmac import set_wallpaper_windows, set_wallpaper_macosx
from .linux import set_wallpaper_linux

def set_wallpaper(path):
    _os = os()
    if _os=='windows':
        log.debug("Windows")
        set_wallpaper_windows(path)
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

def get_default_image_path():
    _os = os()
    if _os=='windows':
        return path.join(HOME, '.flickpaper.jpg')
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

if os() == 'windows':
    HOME = environ.get('USERPROFILE')
    USER = environ.get('USERNAME')
else:
    HOME = environ.get('HOME')
    USER = environ.get('USER')

if __name__=='__main__':
    run()
