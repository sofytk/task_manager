from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from data.task_repository import TaskRepository
from domain.model.task import Task
from domain.model.priority import Priority
from domain.model.category import Category

router = APIRouter(prefix="/tasks", tags=["tasks"])
repository = TaskRepository()


class TaskRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    category: str
    priority: str
    date: str


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    priority: str
    date: str
    is_done: bool


def task_to_response(task: Task) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        category=task.category.name,
        priority=task.priority.name,
        date=task.date,
        is_done=task.is_done,
    )


@router.get("/", response_model=List[TaskResponse])
def get_all_tasks():
    """Get all tasks"""
    tasks = repository.get_all_tasks()
    return [task_to_response(task) for task in tasks]


@router.get("/today", response_model=List[TaskResponse])
def get_today_tasks():
    """Get tasks for today"""
    today = datetime.now().strftime("%d-%m-%Y")
    tasks = repository.get_tasks_by_date(today)
    return [task_to_response(task) for task in tasks]


@router.get("/date/{date}", response_model=List[TaskResponse])
def get_tasks_by_date(date: str):
    """Get tasks for a specific date (format: DD-MM-YYYY)"""
    tasks = repository.get_tasks_by_date(date)
    return [task_to_response(task) for task in tasks]


@router.post("/", response_model=TaskResponse)
def create_task(task_request: TaskRequest):
    """Create a new task"""
    try:
        priority = Priority[task_request.priority]
        category = Category[task_request.category]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid priority or category")

    task = Task(
        id=None,
        date=task_request.date,
        title=task_request.title,
        description=task_request.description,
        priority=priority,
        is_done=False,
        category=category,
    )

    repository.add_task(task)
    return task_to_response(task)


@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: str):
    """Delete a task by ID"""
    tasks = repository.get_all_tasks()
    task_to_delete = None

    for task in tasks:
        if task.id == task_id:
            task_to_delete = task
            break

    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Task not found")

    repository.delete_task(task_to_delete)
    return {"message": "Task deleted successfully", "id": task_id}


@router.get("/sort/{field}", response_model=List[TaskResponse])
def sort_tasks(field: str):
    """Sort tasks by field (priority, date, category, title)"""
    valid_fields = ["priority", "date", "category", "title"]
    if field not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid options: {valid_fields}")

    tasks = repository.get_all_tasks()

    if field == "priority":
        priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        tasks.sort(key=lambda t: priority_order.get(t.priority.name, 3))
    elif field == "date":
        tasks.sort(key=lambda t: t.date)
    elif field == "category":
        tasks.sort(key=lambda t: t.category.name)
    elif field == "title":
        tasks.sort(key=lambda t: t.title)

    return [task_to_response(task) for task in tasks]


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_request: TaskRequest):
    """Update a task"""
    tasks = repository.get_all_tasks()
    task_to_update = None

    for task in tasks:
        if task.id == task_id:
            task_to_update = task
            break

    if not task_to_update:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        priority = Priority[task_request.priority]
        category = Category[task_request.category]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid priority or category")

    task_to_update.title = task_request.title
    task_to_update.description = task_request.description
    task_to_update.category = category
    task_to_update.priority = priority
    task_to_update.date = task_request.date

    repository.update_data(task_to_update)
    return task_to_response(task_to_update)


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
def toggle_task_completion(task_id: str):
    """Toggle task completion status"""
    tasks = repository.get_all_tasks()
    task_to_toggle = None

    for task in tasks:
        if task.id == task_id:
            task_to_toggle = task
            break

    if not task_to_toggle:
        raise HTTPException(status_code=404, detail="Task not found")

    task_to_toggle.is_done = not task_to_toggle.is_done
    repository.update_data(task_to_toggle)
    return task_to_response(task_to_toggle)
