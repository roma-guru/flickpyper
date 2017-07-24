import some_flicker_lib

import optparse
from logging import getLogger
log = getLogger(__name__)

class Flickpaper:
    API_KEY = '23005d9cf8cc185c1c2d17152d03d98b'

    SIZES = ('Square', 'Large Square', 'Thumbnail', 'Small', 'Small 320',
             'Medium', 'Medium 640', 'Medium 800', 'Large', 'Large 1600',
             'Large 2048', 'Original')

    def __init__(self):
        pass
