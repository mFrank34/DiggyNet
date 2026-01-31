# events.py

from server.coordination import state, jobs


def handle_heartbeat(client_id, data):
    state.update(client_id, data)

    outgoing = []

    if data.get("status") == "idle":
        job = jobs.assign_job(client_id)
        if job:
            outgoing.append({"type": "job", "job": job})

    if "job_progress" in data:
        jobs.update_progress(client_id, data["job_progress"])

    if "job_done" in data:
        jobs.complete_job(client_id, data["job_done"])

    return outgoing
