from fastapi import FastAPI, HTTPException
from uvicorn import run

my_app = FastAPI(
    title="Test API",
    description="Just testing my skills",
    version="0.0.1"
)

fake_tasks_db = [
    {"task_id": 1, "task_name": "Изучить Python"},
    {"task_id": 1, "task_name": "Изучить Python"},
    {"task_id": 1, "task_name": "Изучить Python"},
    {"task_id": 1, "task_name": "Изучить Python"},
    {"task_id": 1, "task_name": "Изучить Python"},
    {"task_id": 1, "task_name": "Изучить Python"},
    {"task_id": 2, "task_name": "Подключить Базу Данных"},
    {"task_id": 3, "task_name": "Выучить FastAPI"},
]

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


if __name__ == "__main__":
    run("index:my_app", host="127.0.0.1", port=8000, reload=True)