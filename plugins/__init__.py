"""
Import all the modules
https://stackoverflow.com/a/1057534
"""

import glob
from os.path import dirname, basename, isfile

modules = glob.glob(dirname(__file__) + "/*.py")
All_PLUGINS = [
    basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
]
