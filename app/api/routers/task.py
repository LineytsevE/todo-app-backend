from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_task_service
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services.task import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[Task])
def get_tasks(service: TaskService = Depends(get_task_service)) -> list[Task]:
    return service.list_tasks()


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> Task:
    return service.create_task(payload)


@router.patch("/{task_id}", response_model=Task)
def update_task(
    task_id: str,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> Task:
    return service.update_task(task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
) -> None:
    service.delete_task(task_id)
