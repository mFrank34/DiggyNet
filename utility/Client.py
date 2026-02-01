import requests
import threading
import time
import json

# --- CONFIG ---
SERVER_URL = "http://86.152.155.42:8000"
SERVER_KEY = "d2c0339c250fe8ff5fad6d657d3e8edda4bccde91e7abe7c19f05853df94a274"
HEARTBEAT_INTERVAL = 1  # seconds

# --- STATE ---
running = True
client_id = None
client_key = None

# Fake turtle state
turtle_state = {
    "x": 0,
    "y": 64,
    "z": 0,
    "state": "idle",
    "fuel": 9999
}


# --- FUNCTIONS ---

def register():
    """Register the client with the server to get client ID and key."""
    global client_id, client_key
    print("[INFO] Registering client...")

    try:
        resp = requests.post(
            f"{SERVER_URL}/heartbeat",
            json={"server_key": SERVER_KEY}
        )
    except Exception as e:
        print("[ERROR] Registration failed:", e)
        return False

    print("[DEBUG] Register response:", resp.status_code, resp.text)

    if resp.status_code not in (200, 201):
        print("[ERROR] Registration failed")
        return False

    data = resp.json()
    client_id = data.get("id")
    client_key = data.get("key")

    if not client_id or not client_key:
        print("[ERROR] Server did not return id or key")
        return False

    print(f"[INFO] Registered: ID={client_id}, Key={client_key}")
    return True


def heartbeat_loop():
    """Send heartbeat to server repeatedly, print received jobs/tasks."""
    global running

    while running:
        payload = {
            "id": client_id,
            "key": client_key,
            "x": turtle_state["x"],
            "y": turtle_state["y"],
            "z": turtle_state["z"],
            "state": turtle_state["state"],
            "fuel": turtle_state["fuel"]
        }

        try:
            resp = requests.post(f"{SERVER_URL}/heartbeat", json=payload)
        except Exception as e:
            print("[ERROR] Heartbeat request failed:", e)
            time.sleep(HEARTBEAT_INTERVAL)
            continue

        if resp.status_code != 200:
            print(f"[ERROR] Heartbeat failed: {resp.status_code}, {resp.text}")
            time.sleep(HEARTBEAT_INTERVAL)
            continue

        try:
            data = resp.json()
        except Exception as e:
            print("[ERROR] Failed to parse JSON:", e)
            time.sleep(HEARTBEAT_INTERVAL)
            continue

        # Normalize response
        items = data if isinstance(data, list) else [data]

        if not items or items == [{}]:
            print("[INFO] Idle: no jobs or tasks")
        else:
            for item in items:
                ttype = item.get("type", "unknown")
                print(f"[RECEIVED {ttype.upper()}] {json.dumps(item, indent=2)}")

                if ttype == "task":
                    complete_task(item["task"])

                if ttype == "job":
                    print(f"[INFO] Job received: {item['job']['id']}")

        time.sleep(HEARTBEAT_INTERVAL)


def complete_task(task):
    """Simulate completing a task."""
    print(f"[SIMULATE DONE] Task {task.get('action')} ({task.get('id')})")

    # Report task completion via heartbeat
    payload = {
        "id": client_id,
        "key": client_key,
        "task_done": task.get("id")
    }

    try:
        resp = requests.post(f"{SERVER_URL}/heartbeat", json=payload)
        print("[DEBUG] Task done response:", resp.status_code, resp.text)
    except Exception as e:
        print("[ERROR] Failed to report task done:", e)


def quit_listener():
    """Listen for 'q' to quit."""
    global running
    while running:
        key = input().strip().lower()
        if key == "q":
            running = False
            print("[INFO] Quit signal received, stopping...")


# --- MAIN ---
if __name__ == "__main__":
    if register():
        threading.Thread(target=quit_listener, daemon=True).start()
        heartbeat_loop()

    print("[INFO] Client stopped.")
