# jobs.py

from server import db
from server.coordination import scheduler

from tests.dance import * # adjust path to your test package



def assign_job(client_id):
    job = db.get_next_unassigned_job()
    if not job:
        return None

    chosen = scheduler.choose_turtle_for_job(job)
    if chosen != client_id:
        return None

    db.assign_job(job["id"], client_id)

    start_job(client_id, job)

    return job


def update_progress(client_id, progress):
    db.update_job_progress(progress["job_id"], progress["value"])


def complete_job(client_id, job_id):
    db.complete_job(job_id)
