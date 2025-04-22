from fastapi.testclient import TestClient
from main import app, create_db_and_tables
import os

client = TestClient(app)

# def setup_module(module):
#     # Supprime l'ancienne DB pour des tests propres
#     if os.path.exists("database.db"):
#         os.remove("database.db")
#     create_db_and_tables()

def test_create_task():
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Ceci est une tâche de test",
        "done": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Task"
    assert data["done"] == False

# def test_get_tasks():
#     response = client.get("/tasks")
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#     assert len(data) >= 1

# def test_update_task():
#     response = client.put("/tasks/1", json={
#         "id": 1,
#         "title": "Task Modifiée",
#         "description": "Description modifiée",
#         "done": True
#     })
#     assert response.status_code == 200
#     data = response.json()
#     assert data["title"] == "Task Modifiée"
#     assert data["done"] == True

# def test_delete_task():
#     response = client.delete("/tasks/1")
#     assert response.status_code == 204

#     response = client.get("/tasks/1")
#     assert response.status_code == 404