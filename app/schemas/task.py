from pydantic import BaseModel, ConfigDict


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class TaskCreate(BaseModel):
    title: str
