import logging as log
import json


class NoConfigurationFileError(Exception):
    pass


def load(
    local_path="/etc/mender/mender.conf", global_path="/data/etc/mender/mender.conf"
):
    """Read and return the config from the local and global config files"""
    log.info("Loading the configuration files...")
    global_conf = local_conf = None
    try:
        with open(global_path, "r") as fh:
            global_conf = json.load(fh)
    except FileNotFoundError:
        log.debug(f"Global configuration file not found: {e}")
        pass
    try:
        with open(local_path, "r") as fh:
            local_conf = json.load(fh)
    except FileNotFoundError as e:
        log.debug(f"Local configuration file not found: {e}")
    if not global_conf and not local_conf:
        raise NoConfigurationFileError
    if global_conf and local_conf:
        # Merge the two files, giving precedence to the local configuration
        return {**global_conf, **local_conf}
    if global_conf:
        return global_conf
    return local_conf
