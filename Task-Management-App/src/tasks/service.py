from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from src.tasks.dtos import TaskSchema
from src.user.models import UserModel
from src.utils.exceptions import NotFoundException, UnauthorizedException

class TaskService:
    @staticmethod
    def create_task(db: Session, body: TaskSchema, user: UserModel):
        new_task = TaskModel(
            title=body.title,
            description=body.description,
            is_completed=body.is_completed,
            user_id=user.id,
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    @staticmethod
    def get_tasks(db: Session, user: UserModel):
        return db.query(TaskModel).filter(TaskModel.user_id == user.id).all()

    @staticmethod
    def get_task_by_id(db: Session, task_id: int, user: UserModel):
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise NotFoundException("Task not found")
        if task.user_id != user.id:
            raise UnauthorizedException("You don't have access to this task")
        return task

    @staticmethod
    def update_task(db: Session, task_id: int, body: TaskSchema, user: UserModel):
        task = TaskService.get_task_by_id(db, task_id, user)
        
        for field, value in body.model_dump().items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int, user: UserModel):
        task = TaskService.get_task_by_id(db, task_id, user)
        db.delete(task)
        db.commit()
        return True
