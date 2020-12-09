import base64
import logging as log
import requests
import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


class AuthReqData(object):
    # Identity data
    def __init__(self, id_data, tenant_token, pubkey):
        self.id_data = id_data
        self.tenant_token = tenant_token
        self.pubkey = pubkey


def request(server_url, tenant_token, id_data, private_key):
    print("Authorizing...")
    Client().authorize(server_url, id_data, tenant_token, private_key)
    return True


class Client(object):
    def __init__(self):
        pass

    def authorize(self, server_url, id_data, tenant_token, private_key):
        public_key = private_key.public_key()
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        id_data_json = json.dumps(id_data)
        body = {
            "id_data": id_data_json,
            "pubkey": public_key_pem.decode(),
            "tenant_token": tenant_token,
        }
        # Sign the body
        raw_data = json.dumps(body)
        signature = private_key.sign(
            bytes(raw_data, "utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        # Base 64 encode the signature
        sig = base64.b64encode(signature)
        sig_str = sig.decode()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-MEN-Signature": sig.decode(),
            "Authorization": "API_KEY",
        }
        log.debug(f"Headers: {headers}")
        r = requests.post(
            server_url + "/api/devices/v1/authentication/auth_requests",
            data=raw_data,
            headers=headers,
        )
        log.debug(f"Authorization request returned: {r}")
        # pdb.set_trace()
        if r.status_code == 200:
            log.info("The client successfully authenticated with the Mender server")
        else:
            log.error("The client failed to authorize with the Mender server.")
            log.error(f"Error {r.reason}. code: {r.status_code}")

        print(r.json())
