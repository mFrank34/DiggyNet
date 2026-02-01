from collections import defaultdict
import logging

task_queues = defaultdict(list)
logger = logging.getLogger(__name__)

# Optional: track which clients are doing a looping dance
looping_dances = set()


def enqueue(client_id, task):
    task_queues[client_id].append(task)


def next_task(client_id):
    if task_queues[client_id]:
        task = task_queues[client_id].pop(0)

        # Log AFTER retrieving the task
        logger.info(f"[TASK DISPATCH] → Turtle {client_id}: {task}")

        # If the queue is empty and the client has a looping dance, re-enqueue
        if not task_queues[client_id] and client_id in looping_dances:
            enqueue_dance(client_id)

        return task

    return None


def enqueue_dance(client_id, loop=True):
    """
    Add a dance sequence to the client's queue.
    If loop=True, it will keep re-enqueueing when finished.
    """
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

    # Mark this client as looping dance if requested
    if loop:
        looping_dances.add(client_id)
