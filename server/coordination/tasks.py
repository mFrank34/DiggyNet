from collections import defaultdict

task_queues = defaultdict(list)


def enqueue(client_id, task):
    task_queues[client_id].append(task)


def next_task(client_id):
    if task_queues[client_id]:
        return task_queues[client_id].pop(0)
    return None
