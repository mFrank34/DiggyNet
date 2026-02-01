# server/coordination/events.py
# server/coordination/events.py

import time
from server.coordination import state


def handle_heartbeat(client_id: str, data: dict):
    """
    Coordination-layer heartbeat handler.
    This function existed in your old server and is still expected
    by routes.handle_heartbeat().
    """

    key = data.get("key")

    turtle_data = {
        "status": data.get("status"),
        "location": data.get("location"),
        "last_command": data.get("last_command"),
        "stats": data.get("stats"),
        "vision": data.get("vision"),
        "last_seen": time.time(),
    }

    # Update or create turtle entry
    turtle = state.update_turtle(client_id, key, turtle_data)

    return turtle
