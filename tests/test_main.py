from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "roto-a-proposito"


def test_list_tasks_starts_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task():
    response = client.post("/tasks", json={
        "title": "Mi primera tarea",
        "description": "Descripción de prueba"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Mi primera tarea"
    assert data["completed"] == False
    assert "id" in data


def test_get_task():
    task_id = client.post("/tasks", json={"title": "Tarea de prueba"}).json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_task_not_found():
    response = client.get("/tasks/id-que-no-existe")
    assert response.status_code == 404


def test_complete_task():
    task_id = client.post("/tasks", json={"title": "Completar esto"}).json()["id"]
    response = client.put(f"/tasks/{task_id}", json={
        "title": "Completar esto",
        "completed": True
    })
    assert response.status_code == 200
    assert response.json()["completed"] == True


def test_delete_task():
    task_id = client.post("/tasks", json={"title": "Borrar esto"}).json()["id"]
    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404