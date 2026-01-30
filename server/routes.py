import json


def handle_hello(data):
    turtle_id = data.get("id", "unknown")

    return {
        "message": f"hello {turtle_id} 👋",
        "job": "idle"
    }
