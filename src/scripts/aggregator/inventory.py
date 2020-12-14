# Aggregate inventory
#
# Parses key=value pairs from the inventory scripts on the device
#

import os
import os.path as path
import subprocess

from src.scripts.aggregator.aggregator import ScriptKeyValueAggregator


def aggregate(path="/usr/share/mender/inventory"):
    """Runs all the inventory scripts in 'path', and parses the 'key=value' pairs
    into a data-structure ready for passing it on to the Mender server"""
    keyvals = {}
    for inventory_script in inventory_scripts(path):
        keyvals.update(inventory_script.run())
    return keyvals


def inventory_scripts(inventory_dir):
    """Returns all the inventory scripts in a directory.

    An inventory scripts needs to:

    * Be executable
    * Be located in '/usr/share/mender/inventory'
    """
    scripts = []
    for f in os.listdir(inventory_dir):
        fp = path.join(inventory_dir, f)
        if path.isfile(fp) and os.access(fp, os.X_OK):
            scripts.append(ScriptKeyValueAggregator(fp))
    return scripts
