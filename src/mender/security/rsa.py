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
import base64
import logging as log
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

RSA_key_length = 3072


def generate_key():
    key = rsa.generate_private_key(
        public_exponent=65537,  # https://www.daemonology.net/blog/2009-06-11-cryptographic-right-answers.html
        key_size=RSA_key_length,
    )
    return key


def public_key(private_key):
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return public_key_pem.decode()


def store_key(private_key, path="/path/to/rsa_keys"):
    log.info(f"Storing key to: {path}")
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(path + "/id_rsa", "wb") as key_file:
        # TODO -- set the permissions proper
        os.chmod(path, 0o0755)
        key_file.write(pem)


def load_key(path="/path/to/rsa_keys"):
    log.info(f"Loading key from: {path}")
    with open(path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)
        return private_key


def sign(private_key, data):
    signature = private_key.sign(
        data=bytes(data, "utf-8"), padding=padding.PKCS1v15(), algorithm=hashes.SHA256()
    )
    sig = base64.b64encode(signature)
    return sig.decode()
