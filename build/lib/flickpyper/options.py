import argparse
from os import path
from datetime import date
from flickpyper.common import HOME, get_default_image_path

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
    if res.verbose: print(f"Options: {res}")
    if res.sizes:
        print(', '.join(SIZES))
        sys.exit(0)
    elif res.version:
        print(VERSION)
        sys.exit(0)
    else:
        return res
