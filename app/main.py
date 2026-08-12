from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
import time

app = FastAPI(title="TaskMaster API", version="1.0.0")

tasks = {}


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "taskmaster-api"}


@app.get("/tasks")
def list_tasks():
    return list(tasks.values())


@app.get("/tasks/completed")
def list_completed_tasks():
    return [task for task in tasks.values() if task["completed"]]


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tasks[task_id]


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    task_id = str(uuid.uuid4())
    task_data = {"id": task_id, **task.model_dump()}
    tasks[task_id] = task_data
    return task_data


@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    task_data = {"id": task_id, **task.model_dump()}
    tasks[task_id] = task_data
    return task_data


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    del tasks[task_id]
    return {"message": "Tarea eliminada"}


@app.get("/stress-test")
def stress_test():
    end_time = time.time() + 150
    while time.time() < end_time:
        _ = [i ** 2 for i in range(10000)]
    return {"status": "stress test completado"}