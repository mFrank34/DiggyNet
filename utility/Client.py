# Client.py
from operator import truediv

import requests
import time
import uuid
import threading

# --- configuration ---
SERVER_URL = "http://86.152.155.42:8000"
CLIENT_ID = str(uuid.uuid4())
HEARTBEAT_INTERVAL = 1

# --- program flags ---
running = True


# --- Register Client ---
def register():
    response = requests.post(SERVER_URL + "/heartbeat", json={"client_id": CLIENT_ID})
    if response.status_code == (200, 201):
        print(f"[INFO] Registered client {CLIENT_ID}")
    else:
        print(f"[ERROR] Failed to register client {CLIENT_ID}")


# --- Task ---
def complete(task):
    try:
        resp = requests.post(f"{SERVER_URL}/task_done", json={
            "client_id": CLIENT_ID,
            "task_id": task.get("id")
        })
        if resp.status_code == 200:
            print(f"[DONE] Completed task {task.get('action')}")
        else:
            print(f"[ERROR] Failed to report completion: {resp.status_code}, {resp.text}")
    except Exception as e:
        print("[ERROR] Task completion exception:", e)


# --- Heartbeat checker ---
def heartbeat_loop():
    global running
    while running:
        try:
            resp = requests.post(f"{SERVER_URL}/heartbeat", json={"client_id": CLIENT_ID})
            if resp.status_code != 200:
                print(f"[ERROR] Heartbeat failed: {resp.status_code}")
            else:
                data = resp.json()
                task = data.get("task")
                if task:
                    action = task.get("action")
                    print(f"[TASK] Server sent task: {action}")

                    # Simulate task completion immediately
                    complete(task)
        except Exception as e:
            print("[ERROR] Heartbeat exception:", e)

        time.sleep(HEARTBEAT_INTERVAL)


# --- listen for 'q' to quite ---
def listen_for_quit():
    global running
    while running:
        key = input()
        if key.strip().lower() == "q":
            running = False
            print("[INFO] Quit signal received. Stopping client...")


# --- main ---
if __name__ == "__main__":
    register()

    # Start quit listener in background
    threading.Thread(target=listen_for_quit, daemon=True).start()

    # Start heartbeat loop
    heartbeat_loop()

    print("[INFO] Client stopped.")
