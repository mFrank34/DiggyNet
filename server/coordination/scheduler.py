# scheduler.py

from server.map.manager import manager
from server.map.astar import astar
from server.coordination import state

import json

map_manager = manager()

# Track active jobs in memory
active_jobs = {}


def start_job(client_id, job):
    """
    Compatibility shim for the old scheduler API.
    Records that a turtle has started a job.
    """
    active_jobs[client_id] = job


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def estimate_cost(turtle, job):
    job_type = job["type"]
    payload = json.loads(job["payload"])

    # Dance jobs don't need scheduling logic
    if job_type == "dance":
        return 0

    # Navigation jobs require a target
    if job_type == "go_to":
        target = payload.get("target")
        if target is None:
            return 999999
        return manhattan(turtle["location"], target)

    # Default fallback
    return 999999


def choose_turtle_for_job(job):
    best = None
    best_cost = float("inf")

    for client_id, turtle in state.turtles.items():
        if turtle["status"] != "idle":
            continue

        cost = estimate_cost(turtle, job)
        if cost < best_cost:
            best = client_id
            best_cost = cost

    return best
