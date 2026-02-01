# state.py
import time

turtles = {}


def update_turtle(client_id, key, data):
    turtle = turtles.get(client_id, {})

    turtle["id"] = client_id
    turtle["key"] = key
    turtle["status"] = data.get("status")
    turtle["location"] = data.get("location")
    turtle["last_command"] = data.get("last_command")
    turtle["stats"] = data.get("stats")
    turtle["vision"] = data.get("vision")
    turtle["last_seen"] = time.time()

    turtles[client_id] = turtle
    return turtle
