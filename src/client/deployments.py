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
import requests
import logging as log
import json

link = "https://hosted.mender.io/api/devices/v1/deployments"

# TODO -- Device-type is needed, as well as artifact_name!
def request(
    server_url,
    JWT,
    device_type=None,
    artifact_name=None,
    artifact_path="tests/data/artifact.mender",
):
    if not device_type:
        log.error("No device_type found. Update cannot proceed")
        return
    if not artifact_name:
        log.error("No artifact_Name found. Update cannot proceed")
        return
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + JWT}
    r = requests.get(
        server_url + "/api/devices/v1/deployments/device/deployments/next",
        headers=headers,
        params={"artifact_name": artifact_name, "device_type": device_type},
    )
    log.debug(f"update: request: {r}")
    log.error(f"Error {r.reason}. code: {r.status_code}")
    if r.status_code == 200:
        log.info(f"New update available: {r.text}")
        # TODO - Verify the unmarshaling, for now take it for granted
        update_json = r.json()
        # log.debug(f"")
        # import pdb
        # pdb.set_trace()
        update_id = update_json.get("id", "")
        update_url = update_json["artifact"]["source"]["uri"]

        response = requests.get(update_url, stream=True)

        with open(artifact_path, "wb") as fh:
            for data in response.iter_content():
                fh.write(data)
    elif r.status_code == 204:
        log.info("No new update available}")
    else:
        log.debug(f"{r.json()}")
        log.error("Error while fetching update")
