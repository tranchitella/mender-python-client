# Aggregate identity
#
# Parses key=value pairs from the identity scripts on the device
#

import os
import logging as log
import subprocess

from src.scripts.aggregator.aggregator import ScriptKeyValueAggregator


def aggregate(path="/usr/share/mender/identity"):
    """Runs the identity script in 'path', and parses the 'key=value' pairs
    into a data-structure ready for passing it on to the Mender server"""
    log.info("Aggregating the device identity attributes...")
    identity_data = {}
    if os.path.isfile(path) and os.access(path, os.X_OK):
        identity_data = ScriptKeyValueAggregator(path).run()
    log.debug(f"Aggregated identity data: {identity_data}")
    return identity_data
