"""
Import all the modules
https://stackoverflow.com/a/1057534
"""

import glob
from os.path import basename, dirname, isfile

NON_PLUGIN_MODULES = {"__init__", "commands", "utils"}

modules = glob.glob(dirname(__file__) + "/*.py")
All_PLUGINS = [
    basename(f)[:-3]
    for f in modules
    if isfile(f) and basename(f)[:-3] not in NON_PLUGIN_MODULES
]
