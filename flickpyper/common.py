import sys
from os import environ, path, remove

def os():
    host_os = sys.platform
    if host_os in ('cygwin', 'win32'):
        return 'windows'
    elif host_os in ('darwin',):
        return 'macosx'
    elif host_os in ('linux',):
        return 'linux'
    elif host_os in ('solaris', 'bsd'):
        return 'unix'
    else:
        return 'unknown'

def save_file(url, dst):
    import wget
    if path.isfile(dst): remove(dst)
    wget.download(url, dst)

if os() == 'windows':
    HOME = environ.get('USERPROFILE')
    USER = environ.get('USERNAME')
else:
    HOME = environ.get('HOME')
    USER = environ.get('USER')

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
    else:
        print("Unknown OS, exiting")
        sys.exit(-1)
