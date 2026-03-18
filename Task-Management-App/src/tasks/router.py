from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.tasks.dtos import TaskSchema, TaskResponseSchema
from src.tasks.service import TaskService
from src.utils.helpers import get_current_user
from src.user.models import UserModel

task_routes = APIRouter(prefix="/tasks")

@task_routes.post(
    "/", 
    response_model=TaskResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task"
)
def create_task(
    body: TaskSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return TaskService.create_task(db, body, user)

@task_routes.get(
    "/",
    response_model=List[TaskResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Get all tasks for current user"
)
def get_all_tasks(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return TaskService.get_tasks(db, user)

@task_routes.get(
    "/{task_id}",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get task by ID"
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return TaskService.get_task_by_id(db, task_id, user)

@task_routes.put(
    "/{task_id}",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Update a task"
)
def update_task(
    task_id: int,
    body: TaskSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return TaskService.update_task(db, task_id, body, user)

@task_routes.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    TaskService.delete_task(db, task_id, user)
    return None
