import requests
import logging as log

link = "https://hosted.mender.io/api/devices/v1/deployments"

# TODO -- Device-type is needed, as well as artifact_name!
def request(
    server_url,
    JWT,
    device_type="qemux86-64",
    artifact_name="release-0.1",
    artifact_path="tests/data/",
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
        log.info("No new update available}")
    elif r.status_code == 204:
        log.info(f"New update available: {r.text}")
    else:
        log.debug(f"{r.json()}")
        log.error("Error while fetching update")
