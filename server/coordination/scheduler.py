# scheduler.py

from server.map.manager import manager
from server.map.astar import astar
from server.coordination import state

map_manager = manager()


def estimate_cost(turtle, job):
    start = turtle["location"]
    goal = job["target"]

    path = astar(map_manager, start, goal)
    if not path:
        return float("inf")

    return len(path)


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
