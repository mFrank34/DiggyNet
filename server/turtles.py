# turtles.py
import time

turtles = {}

def register(turtle_id, status="idle"):
    turtles[turtle_id] = {
        "status": status,
        "last_seen": time.time()
    }

def heartbeat(turtle_id, status="idle"):
    if turtle_id not in turtles:
        register(turtle_id, status)
    else:
        turtles[turtle_id]["status"] = status
        turtles[turtle_id]["last_seen"] = time.time()

def get_all():
    return turtles
