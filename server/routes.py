# routes.py

from server.coordination import events


def handle_heartbeat(data):
    client_id = data["id"]

    # Let coordination layer process the heartbeat
    actions = events.handle_heartbeat(client_id, data)

    return {
        "actions": actions
    }
