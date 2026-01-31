# event.py
from server.coordination import state, jobs, tasks


def handle_heartbeat(client_id, data):
    state.update(client_id, data)

    outgoing = []

    status = data.get("status", "idle")

    # 1. Assign a job if idle
    if status == "idle":
        job = jobs.assign_job(client_id)
        if job:
            outgoing.append({"type": "job", "job": job})

    # 2. Handle job progress
    if "job_progress" in data:
        jobs.update_progress(client_id, data["job_progress"])

    # 3. Handle job completion
    if "job_done" in data:
        jobs.complete_job(client_id, data["job_done"])

    # 4. Send next task (THIS WAS MISSING)
    task = tasks.next_task(client_id)
    if task:
        outgoing.append({"type": "task", "task": task})

    return outgoing
