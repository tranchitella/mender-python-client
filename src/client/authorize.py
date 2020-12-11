import logging as log
import requests
import json
import src.security.key as key


class AuthReqData(object):
    # Identity data
    def __init__(self, id_data, tenant_token, pubkey):
        self.id_data = id_data
        self.tenant_token = tenant_token
        self.pubkey = pubkey


def request(server_url, tenant_token, id_data, private_key):
    print("Authorizing...")
    return Client().authorize(server_url, id_data, tenant_token, private_key)


class Client(object):
    def __init__(self):
        pass

    def authorize(self, server_url, id_data, tenant_token, private_key):
        id_data_json = json.dumps(id_data)
        public_key = key.public_key(private_key)
        log.debug(f"authorize: Public key: {public_key}")
        body = {
            "id_data": id_data_json,
            "pubkey": public_key,
            "tenant_token": tenant_token,
        }
        # Sign the body
        raw_data = json.dumps(body)
        log.debug(f"Body signature: {key.sign(private_key, raw_data)}")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-MEN-Signature": key.sign(private_key, raw_data),
            "Authorization": "API_KEY",
        }
        log.debug(f"Headers: {headers}")
        log.debug(f"Body: {raw_data}")
        r = requests.post(
            server_url + "/api/devices/v1/authentication/auth_requests",
            data=raw_data,
            headers=headers,
        )
        log.debug(f"Authorization request returned: {r}")
        print(r.json())
        if r.status_code == 200:
            log.info("The client successfully authenticated with the Mender server")
            return True
        else:
            log.error("The client failed to authorize with the Mender server.")
            log.error(f"Error {r.reason}. code: {r.status_code}")
            return False
