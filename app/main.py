from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

# FastAPI crea la aplicación y genera documentación interactiva automática en /docs
app = FastAPI(title="TaskMaster API", version="1.0.0")

# Almacenamiento en memoria — se resetea cada vez que la app se reinicia.
# En un proyecto real sería una base de datos, pero para aprender CI/CD
# y despliegue no la necesitamos, así mantenemos el foco en DevOps, no en BD.
tasks = {}

# Pydantic define el "molde" de una tarea y valida tipos automáticamente.
# Si alguien envía datos mal formados, FastAPI responde el error solo.
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


@app.get("/health")
def health_check():
    # Endpoint crítico: ECS y CloudWatch lo van a llamar para saber si la app está viva
    return {"status": "ok", "service": "taskmaster-api"}


@app.get("/tasks")
def list_tasks():
    return list(tasks.values())


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tasks[task_id]


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    task_id = str(uuid.uuid4())  # genera un ID único, ej: "a3f8c2d1-..."
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

import time

@app.get("/stress-test")
def stress_test():
    # Endpoint temporal solo para probar la alarma de CPU alta
    # Genera carga intensa de CPU durante unos segundos
    end_time = time.time() + 150
    while time.time() < end_time:
        _ = [i ** 2 for i in range(10000)]
    return {"status": "stress test completado"}