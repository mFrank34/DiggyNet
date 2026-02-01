# startup.py

import json, os, uuid
from fastapi import FastAPI


def register_startup_event(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        file_path = "server_data.json"

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                app.state.server_key = data.get("server_key")
        else:
            key = str(uuid.uuid4())
            data = {"server_key": key}
            with open(file_path, "w") as f:
                json.dump(data, f)
            app.state.server_key = key

        print("Server key initialized:", app.state.server_key)
