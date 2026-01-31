# dance.py
from server import db
from server.coordination import tasks


def create_dance_job():
    return db.create_job("dance", {})


def start_job(client_id, job):
    job_type = job["type"]

    if job_type == "dance":
        tasks.enqueue_dance(client_id)
