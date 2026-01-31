# state.py
import time

turtles = {}


def update(client_id, data):
    turtles[client_id] = {
        "last_seen": time.time(),
        "status": data.get("status", "idle"),
        "location": tuple(data.get("location", (0, 0, 0))),
        "job_id": data.get("job_id")
    }
