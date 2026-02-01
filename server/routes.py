# routes.py

from server.coordination import events
from server.coordination import tasks
from server import db
from coordination import scheduler

def handle_heartbeat(data):
    client_id = data["id"]

    # Let coordination layer update turtle state
    events.handle_heartbeat(client_id, data)

    response = []

    # Assign job if idle
    job = db.next_pending_job()
    if job:
        assigned = scheduler.choose_turtle_for_job(job)
        if assigned == client_id:
            db.start_job(job["id"], client_id)
            scheduler.start_job(client_id, job)
            response.append({
                "type": "job",
                "job": job
            })

    # Send next task
    task = tasks.next_task(client_id)
    if task:
        response.append({
            "type": "task",
            "task": task
        })

    return response
