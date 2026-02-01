# debug_client.py
import requests
import threading
import time
import json
import os

# --- Configuration ---
SERVER_URL = "http://86.152.155.42:8000"
SERVER_KEY_FILE = "server_key.json"  # file to read server key from
HEARTBEAT_INTERVAL = 1
STATE_FILE = "client_state.json"

# --- Program flags ---
running = True
client_id = None
client_key = None
server_key = None


# --- Load server key ---
def load_server_key():
    global server_key
    if os.path.exists(SERVER_KEY_FILE):
        with open(SERVER_KEY_FILE, "r") as f:
            server_key = json.load(f).get("server_key")
            print(f"[INFO] Loaded server key: {server_key}")
    else:
        raise FileNotFoundError(f"{SERVER_KEY_FILE} not found. Save the server key here.")


# --- Load saved client state ---
def load_state():
    global client_id, client_key
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            client_id = data.get("id")
            client_key = data.get("key")
            if client_id and client_key:
                print(f"[INFO] Loaded saved client state: ID={client_id}, Key={client_key}")


# --- Save client state ---
def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump({"id": client_id, "key": client_key}, f)
        print(f"[INFO] Client state saved.")


# --- Register Client ---
def register():
    global client_id, client_key
    try:
        resp = requests.post(
            f"{SERVER_URL}/heartbeat",
            json={"server_key": server_key}
        )
        if resp.status_code in (200, 201):
            data = resp.json()
            client_id = data.get("id")
            client_key = data.get("key")
            print(f"[INFO] Registered client: ID={client_id}, Key={client_key}")
            return True
        else:
            print(f"[ERROR] Failed to register: {resp.status_code}, {resp.text}")
            return False
    except Exception as e:
        print("[ERROR] Exception during registration:", e)
        return False


# --- Complete task ---
def complete(task):
    try:
        resp = requests.post(
            f"{SERVER_URL}/task_done",
            json={"id": client_id, "key": client_key, "task_id": task.get("id")}
        )
        if resp.status_code == 200:
            print(f"[DONE] Completed task: {task.get('action')}")
        else:
            print(f"[ERROR] Failed to report task completion: {resp.status_code}, {resp.text}")
    except Exception as e:
        print("[ERROR] Task completion exception:", e)


# --- Heartbeat loop ---
def heartbeat_loop():
    global running
    while running:
        try:
            resp = requests.post(
                f"{SERVER_URL}/heartbeat",
                json={"id": client_id, "key": client_key}
            )
            if resp.status_code != 200:
                print(f"[ERROR] Heartbeat failed: {resp.status_code}, {resp.text}")
            else:
                data = resp.json()
                tasks = data.get("task")
                # Tasks can be a single task or a list
                if tasks:
                    if isinstance(tasks, dict):
                        tasks = [tasks]
                    for task in tasks:
                        print(f"[TASK] Server sent task: {task.get('action')}")
                        complete(task)
        except Exception as e:
            print("[ERROR] Heartbeat exception:", e)

        time.sleep(HEARTBEAT_INTERVAL)


# --- Listen for 'q' to quit ---
def listen_for_quit():
    global running
    while running:
        key = input()
        if key.strip().lower() == "q":
            running = False
            print("[INFO] Quit signal received. Stopping client...")


# --- Main ---
if __name__ == "__main__":
    load_server_key()
    load_state()

    if register():
        # Start quit listener
        threading.Thread(target=listen_for_quit, daemon=True).start()
        # Start heartbeat loop
        heartbeat_loop()

    print("[INFO] Client stopped.")
