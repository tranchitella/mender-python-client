import logging as log

from src.scripts.aggregator.aggregator import ScriptKeyValueAggregator


def get(path="/var/lib/mender/device_type"):
    try:
        with open(path) as fh:
            device_type = ScriptKeyValueAggregator(path).collect()
            if len(device_type.keys()) > 1:
                log.error(
                    "Multiple key=value pairs found in the device_type file. Only one is allowed"
                )
                return
            return device_type
    except FileNotFoundError:
        log.error(f"No device_type file found in {path}")
        return None
    except Exception as e:
        log.error(f"Error: {e}")
