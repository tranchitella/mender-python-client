# Copyright 2020 Northern.tech AS
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
# Aggregate inventory
#
# Parses key=value pairs from the inventory scripts on the device
#

import logging as log
import os
import os.path as path
import subprocess

from src.scripts.aggregator.aggregator import ScriptKeyValueAggregator
import src.scripts.devicetype as devicetype
import src.scripts.artifactinfo as artifactinfo


def aggregate(path="/usr/share/mender/inventory"):
    """Runs all the inventory scripts in 'path', and parses the 'key=value' pairs
    into a data-structure ready for passing it on to the Mender server"""
    keyvals = {}
    for inventory_script in inventory_scripts(path):
        keyvals.update(inventory_script.run())
    dt = devicetype.get("tests/data/mender/device_type")
    log.info(f"Found the device type: {dt}")
    keyvals.update(dt)
    an = artifactinfo.get("tests/data/mender/artifact_info")
    log.info(f"Found the device type: {dt}")
    keyvals.update(an)
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
