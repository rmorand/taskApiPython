from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select

from Task import Task
from TaskCreate import TaskCreate
from TaskUpdate import TaskUpdate

app = FastAPI()

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'API de gestion des tâches"}

# @app.get("/tasks", response_model=list[Task])
# def read_tasks(session: Session = Depends(lambda: Session(engine))):
#     tasks = session.exec(select(Task)).all()
#     return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, session: Session = Depends(lambda: Session(engine))):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return task

@app.post("/tasks", response_model=Task)
def create_task(task: Task, session: Session = Depends(lambda: Session(engine))):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: Task, session: Session = Depends(lambda: Session(engine))):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    task.title = task_data.title
    task.description = task_data.description
    task.done = task_data.done
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(lambda: Session(engine))):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    session.delete(task)
    session.commit()
