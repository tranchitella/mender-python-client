import base64
import os
import logging as log

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

RSA_key_length = 3072


def generate_key():
    log.debug("generate_key: ")
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
        bytes(data, "utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256(),
    )
    sig = base64.b64encode(signature)
    return sig.decode()
