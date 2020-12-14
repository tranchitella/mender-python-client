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
import os
import logging as log

import src.security.key as key

# TODO -- What to do here (?)
private_key_path = "./tests/data/keys/"


def now():
    log.info("Bootstrapping the device")
    # TODO -- respect the force-bootstrap argument
    private_key = key_already_generated()
    log.info(f"The returned private_key: {private_key}")
    if not private_key:
        log.info("Generating a new RSA key pair")
        private_key = key.generate_key()
        key.store_key(private_key, private_key_path)
    # TODO - Should we try do authorize (?)
    log.info("Device bootstrapped successfully")
    return private_key


def key_already_generated():
    log.debug("Checking if a key already exists for the device")
    try:
        return key.load_key(private_key_path + "id_rsa")
    except FileNotFoundError:
        return None
    except Exception as e:
        log.error(e)
    return None
