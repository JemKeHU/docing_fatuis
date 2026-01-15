from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uvicorn import run
from random import randint

my_app = FastAPI(
    title="Test API",
    description="Just testing my skills",
    version="0.0.1"
)

class STaskAdd(BaseModel):
    name: str = Field(min_length=2, max_length=100, description="Task Name")
    description: str | None = Field(default=None, min_length=0, max_length=300, description="Task Description")
    priority: int = Field(default=1, le=5, description="Task Priority")

class STaskAddBase(STaskAdd):
    pass

class STaskAddResponse(STaskAddBase):
    id: int = Field(...)

fake_tasks_db = []

@my_app.get("/tasks/{task_id}")
async def get_task_by_it(task_id: int):
    for task in fake_tasks_db:
        if task["task_id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@my_app.get("/tasks")
async def get_tasks(limit: int = 10, offset: int = 0, keyword: str | None = None):
    filtered_tasks = []
    if keyword:
        for task in fake_tasks_db:
            if keyword.lower() in task["task_name"].lower():
                filtered_tasks.append(task)
    else:
        filtered_tasks = fake_tasks_db
    return filtered_tasks[offset:offset + limit]

@my_app.post("/tasks")
async def add_task(task: STaskAdd):
    task_dict = task.model_dump()
    task_dict["id"] = randint(100, 999)
    fake_tasks_db.append(task_dict)
    return {"ok": True, "message": "Task was added", "task": task_dict}


if __name__ == "__main__":
    run("index:my_app", host="127.0.0.1", port=8000, reload=True)