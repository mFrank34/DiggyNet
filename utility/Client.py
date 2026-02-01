# debug_client.py
import requests
import threading
import time
import json

SERVER_URL = "http://86.152.155.42:8000"
SERVER_KEY = "59bc2c79fb3b6a978e335d7f2922381be294277c6e5d81c3f07f1d190d8150c8"
HEARTBEAT_INTERVAL = 1

running = True
client_id = None
client_key = None


# --- Register client ---
def register():
    global client_id, client_key
    print("[INFO] Registering client...")
    resp = requests.post(f"{SERVER_URL}/heartbeat", json={"server_key": SERVER_KEY})
    print("[DEBUG] Register response:", resp.status_code, resp.text)
    if resp.status_code not in (200, 201):
        print("[ERROR] Registration failed")
        return False
    data = resp.json()
    client_id = data["id"]
    client_key = data["key"]
    print(f"[INFO] Registered with ID={client_id}")
    return True


# --- Complete task ---
def complete_task(task):
    print(f"[TASK DONE] {task.get('action')} ({task.get('id')})")
    resp = requests.post(
        f"{SERVER_URL}/task_done",
        json={"id": client_id, "key": client_key, "task_id": task.get("id")}
    )
    print("[DEBUG] Task done response:", resp.status_code, resp.text)


# --- Heartbeat loop ---
def heartbeat_loop():
    global running
    while running:
        try:
            resp = requests.post(
                f"{SERVER_URL}/heartbeat",
                json={"id": client_id, "key": client_key}
            )
        except Exception as e:
            print("[ERROR] Heartbeat request exception:", e)
            time.sleep(HEARTBEAT_INTERVAL)
            continue

        # Check response status
        if resp.status_code != 200:
            print(f"[ERROR] Heartbeat failed: {resp.status_code}, {resp.text}")
            time.sleep(HEARTBEAT_INTERVAL)
            continue

        # Parse response safely
        try:
            data = resp.json()
        except Exception as e:
            print("[ERROR] Failed to parse heartbeat JSON:", e)
            time.sleep(HEARTBEAT_INTERVAL)
            continue

        # Normalize tasks to a list
        tasks = []
        if isinstance(data, dict):
            tasks_data = data.get("task")
            if tasks_data:
                if isinstance(tasks_data, dict):
                    tasks = [tasks_data]
                elif isinstance(tasks_data, list):
                    tasks = tasks_data
        elif isinstance(data, list):
            tasks = data

        # Process tasks
        for task in tasks:
            print("[TASK RECEIVED]", task)
            complete_task(task)

        time.sleep(HEARTBEAT_INTERVAL)


# --- Quit listener ---
def quit_listener():
    global running
    while running:
        if input().strip().lower() == "q":
            running = False
            print("[INFO] Quit signal received, stopping...")


# --- Main ---
if __name__ == "__main__":
    if register():
        threading.Thread(target=quit_listener, daemon=True).start()
        heartbeat_loop()
    print("[INFO] Client stopped.")
