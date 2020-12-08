import logging as log
import requests


class AuthReqData(object):
    # Identity data
    def __init__(self, id_data, tenant_token, pubkey):
        self.id_data = id_data
        self.tenant_token = tenant_token
        self.pubkey = pubkey


def request(id_data, tenant_token, public_key):
    print("Authorizing...")
    Client().authorize()
    return True


class Client(object):
    def __init__(self):
        pass

    def authorize(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-MEN-Signature": "string",
            "Authorization": "API_KEY",
        }
        r = requests.post(
            "https://hosted.mender.io/api/devices/v1/authentication/auth_requests",
            headers=headers,
        )
        log.debug(f"Authorization request returned: {r}")
        if r.status_code == 200:
            log.info("The client successfully authenticated with the Mender server")
        else:
            log.error("The client failed to authorize with the Mender server.")
            log.error(f"Error {r.reason}. code: {r.status_code}")

        print(r.json())
