from server import db
from server.coordination import scheduler

def assign_job(client_id):
    job = db.get_next_unassigned_job()
    if not job:
        return None

    chosen = scheduler.choose_turtle_for_job(job)
    if chosen != client_id:
        return None

    db.assign_job(job["id"], client_id)
    return job
