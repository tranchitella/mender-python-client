import logging as log
import json


class NoConfigurationFileError(Exception):
    pass


class Config(dict):
    """A dictionary for storing Mender configuration values"""

    def __init__(self, *args, **kw):
        super(Config, self).__init__(self, *args, **kw)
        self.__dict__ = self

    # TODO - handle non-existing keys, or explicitly map to all acceptable
    # values


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
        b = {**global_conf, **local_conf}
        c = Config()
        c.update(b)
        return c
    if global_conf:
        c = Config()
        c.update(global_conf)
        return c
    c = Config()
    c.update(local_conf)
    return c
