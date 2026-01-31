# tasks.py
from collections import defaultdict

task_queues = defaultdict(list)


def enqueue(client_id, task):
    task_queues[client_id].append(task)


def next_task(client_id):
    if task_queues[client_id]:
        return task_queues[client_id].pop(0)
    return None


def enqueue_dance(client_id):
    sequence = [
        {"action": "move_left"},
        {"action": "move_right"},
        {"action": "move_forward"},
        {"action": "move_back"},
        {"action": "move_left"},
        {"action": "move_right"},
    ]
    for step in sequence:
        enqueue(client_id, step)
