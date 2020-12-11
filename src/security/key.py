import src.security.rsa as rsa

import os
import logging as log


class Key(object):
    """Class for holding the device key"""

    def __init__(self):
        pass

    def sign(self, data):
        pass

    def pub_key(self):
        pass

    def generate(self):
        pass

    def load(self):
        pass


def generate_key():
    log.debug("generate_key: ")
    private_key = rsa.generate_key()
    return private_key


def public_key(private_key):
    log.debug("key: public_key()")
    return rsa.public_key(private_key)


def store_key(private_key, path="/path/to/rsa_keys"):
    log.info(f"Storing key to: {path}")
    rsa.store_key(private_key, path)


def load_key(path="/path/to/rsa_keys"):
    log.info(f"Loading key from: {path}")
    return rsa.load_key(path)


def sign(private_key, data):
    log.debug("key: Signing the message body")
    return rsa.sign(private_key, data)
