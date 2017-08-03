import sys

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

def save_file(url, dst):
    import wget
    remove(dst)
    wget.download(url, dst)
