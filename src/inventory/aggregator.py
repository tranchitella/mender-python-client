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
        ss = output.stdout.decode()
        for line in ss.split("\n"):
            if line == "":
                continue
            arr = line.strip().split("=")
            # TODO -- handle, and pretty up!
            # print(f"aggregated line: {line}")
            assert len(arr) == 2, f"Real len: {len(arr)}"
            key, val = arr[0], arr[1]
            # print(f"dict: {self.vals}")
            l = self.vals.get(key, [])
            l.append(val)
            self.vals[key] = l
        return self.vals


# class InventoryKeyVal(dict):
