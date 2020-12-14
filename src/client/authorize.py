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
        log.debug(f"response: {r.text}")
        if r.status_code == 200:
            log.info("The client successfully authenticated with the Mender server")
            JWT=r.text
            return JWT
        else:
            log.error("The client failed to authorize with the Mender server.")
            log.error(f"Error {r.reason}. code: {r.status_code}")
            log.error(f"json: {r.json()}")
            return None
