from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository
from app.schemas.task import Task, TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repo = TaskRepository(db)

    def list_tasks(self) -> list[Task]:
        tasks = self.task_repo.get_all()
        return [Task.model_validate(task) for task in tasks]

    def create_task(self, task_create: TaskCreate) -> Task:
        task = self.task_repo.create(title=task_create.title)
        self.db.commit()
        return Task.model_validate(task)

    def update_task(self, task_id: str, task_update: TaskUpdate) -> Task:
        task_for_update = self.task_repo.get_by_id(task_id=task_id)
        if task_for_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        task_for_update.title = (
            task_update.title
            if task_update.title is not None
            else task_for_update.title
        )
        task_for_update.completed = (
            task_update.completed
            if task_update.completed is not None
            else task_for_update.completed
        )
        self.db.commit()
        return Task.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> None:
        task_for_delete = self.task_repo.get_by_id(task_id=task_id)
        if task_for_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        self.task_repo.delete(task_for_delete)
        self.db.commit()
