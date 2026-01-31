from turtles import *

counter = 1

def handle_heartbeat(data):
    global counter

    turtle_id = data.get("id")
    status = data.get("status", "idle")

    if not turtle_id:
        turtle_id = f"turtle_{counter:02}"
        counter += 1
        print(f"Assigned {turtle_id}", flush = True)
    else:
        print(f"Turtle: {turtle_id} Heartbeat ({status})", flush = True)

    heartbeat(turtle_id, status)

    return {
        "ok": True,
        "id": turtle_id,
        "known_turtles": len(get_all())
    }
