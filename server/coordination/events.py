# event.py (FastAPI version)

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Tuple, Dict, Any, List

from server.coordination import tasks, state
from server import db
from server.coordination import scheduler

router = APIRouter()


# --- Heartbeat Request Model ---
class Heartbeat(BaseModel):
    id: Optional[str]
    key: Optional[str]
    role: Optional[str] = None
    status: str
    task: Optional[Dict[str, Any]] = None
    last_command: Optional[Dict[str, Any]] = None
    location: Optional[Tuple[int, int, int]] = None
    stats: Optional[Dict[str, Any]] = None
    vision: Optional[Dict[str, Any]] = None


# --- Heartbeat Endpoint ---
@router.post("/heartbeat")
async def heartbeat(data: Heartbeat) -> List[Dict[str, Any]]:
    client_id = data.id
    key = data.key

    # 1. Register or authenticate turtle
    turtle = state.update_turtle(client_id, key, data.dict())

    response: List[Dict[str, Any]] = []

    # 2. If turtle is idle, try to assign a job
    if turtle["status"] == "idle":
        job = db.next_pending_job()
        if job:
            assigned = scheduler.choose_turtle_for_job(job)
            if assigned == turtle["id"]:
                db.start_job(job["id"], turtle["id"])
                scheduler.start_job(turtle["id"], job)
                response.append({
                    "type": "job",
                    "job": job
                })

    # 3. Send next task if any
    task = tasks.next_task(turtle["id"])
    if task:
        response.append({
            "type": "task",
            "task": task
        })

    return response
