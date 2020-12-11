import requests
import logging as log
import json

link = "https://hosted.mender.io/api/devices/v1/deployments"

# TODO -- Device-type is needed, as well as artifact_name!
def request(
    server_url,
    JWT,
    device_type="qemux86-64",
    artifact_name="release-0.1",
    artifact_path="tests/data/artifact.mender",
):
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
