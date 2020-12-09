# Aggregate identity
#
# Parses key=value pairs from the identity scripts on the device
#

import os
import logging as log
import subprocess


def aggregate(path="/usr/share/mender/identity"):
    """Runs the identity script in 'path', and parses the 'key=value' pairs
    into a data-structure ready for passing it on to the Mender server"""
    log.info("Aggregating the device identity attributes...")
    identity_data = {}
    if os.path.isfile(path) and os.access(path, os.X_OK):
        identity_data = IdentityScript(path).run()
    log.debug(f"Aggregated identity data: {identity_data}")
    return identity_data


class IdentityScript(object):
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
