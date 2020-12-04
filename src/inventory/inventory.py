# Aggregate inventory
#
# Parses key=value pairs from the inventory scripts on the device
#

import os
import os.path as path
import subprocess


def aggregate(path="/usr/share/mender/inventory"):
    """Runs all the inventory scripts in 'path', and parses the 'key=value' pairs
    into a data-structure ready for passing it on to the Mender server"""
    for inventory_script in inventory_scripts(path):
        inventory_script.run()


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
            scripts.append(InventoryScript(fp))
    return scripts


class InventoryScript(object):
    def __init__(self, script_path):
        self.script_path = script_path
        self.vals = {}

    def run(self):
        # TODO -- Set a proper timeout
        output = subprocess.run(self.script_path, stdout=subprocess.PIPE, timeout=100)
        # Parse the output
        for line in str(output.stdout).split("\n"):
            print(line)
            arr = line.strip().split("=")
            # TODO -- handle, and pretty up!
            assert len(arr) == 2
            key, val = arr[0], arr[1]
            vals = self.vals.get(key, [])
            vals.append(val)


# class InventoryKeyVal(dict):
