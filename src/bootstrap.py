import os
import logging as log

import src.rsa as rsa

# TODO -- What to do here (?)
private_key_path = "./tests/data/keys/"


def now():
    log.info("Bootstrapping the device")
    # TODO -- respect the force-bootstrap argument
    private_key = key_already_generated()
    log.info(f"The returned private_key: {private_key}")
    if not private_key:
        log.info("Generating a new RSA key pair")
        private_key = generate_key()
        rsa.store_key(private_key, private_key_path)
    # TODO - Should we try do authorize (?)
    log.info("Device bootstrapped successfully")
    return private_key


def key_already_generated():
    log.debug("Checking if a key already exists for the device")
    try:
        return rsa.load_key(private_key_path + "id_rsa")
    except FileNotFoundError:
        return None
    except Exception as e:
        log.error(e)
    return None


def generate_key():
    key = rsa.generate_key()
    return key
