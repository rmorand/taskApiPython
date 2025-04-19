from fastapi import FastAPI, HTTPException
from typing import Optional, List
from Task import Task
from TaskCreate import TaskCreate
from TaskUpdate import TaskUpdate

app = FastAPI()

tasks: List[Task] = []
next_id = 1

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'API de gestion des tâches"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Tâche non trouvée")

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    global next_id
    new_task = Task(id=next_id, title=task.title, description=task.description)
    tasks.append(new_task)
    next_id += 1
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task.id == task_id:
            if task_update.title is not None:
                task.title = task_update.title
            if task_update.description is not None:
                task.description = task_update.description
            if task_update.done is not None:
                task.done = task_update.done
            return task
    raise HTTPException(status_code=404, detail="Tâche non trouvée")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[i]
            return
    raise HTTPException(status_code=404, detail="Tâche non trouvée")
