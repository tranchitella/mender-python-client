import requests
import logging as log
import json

link = "https://hosted.mender.io/api/devices/v1/inventory"


def request(server_url, JWT, inventory_data):
    log.debug(
        f"inventory request: server_url: {server_url}\nJWT: {JWT}\ninventory_data: {inventory_data}"
    )
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + JWT}
    log.debug(f"inventory headers: {headers}")
    raw_data = json.dumps([{"name": k, "value": v} for k,v in inventory_data.items()])
    log.debug(f"inventory: raw_data: {raw_data}")
    r = requests.put(
        server_url + "/api/devices/v1/inventory/device/attributes",
        headers=headers,
        data=raw_data,
    )
    log.debug(f"inventory response: {r}")
    log.error(f"Error {r.reason}. code: {r.status_code}")
    if r.status_code != 200:
        log.error(f"{r.json()}")
