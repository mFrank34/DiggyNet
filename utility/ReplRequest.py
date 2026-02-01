import requests

SERVER_URL = "http://86.152.155.42:8000"
server_key = "59bc2c79fb3b6a978e335d7f2922381be294277c6e5d81c3f07f1d190d8150c8"

resp = requests.post(f"{SERVER_URL}/heartbeat", json={"server_key": server_key})
print(resp.status_code, resp.text)
