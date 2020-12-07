import requests


class AuthReqData(object):
    # Identity data
    def __init__(self, id_data, tenant_token, pubkey):
        self.id_data = id_data
        self.tenant_token = tenant_token
        self.pubkey = pubkey


def attempt():
    print("Authorizing...")
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

        print(r.json())
