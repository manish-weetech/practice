from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.crud_item import item as crud_item
from app.schemas.item import ItemResponseSchema, ItemSchema, ItemUpdateSchema
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[ItemResponseSchema])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    if current_user.role == "admin":
        from app.models.item import Item
        items = db.query(Item).offset(skip).limit(limit).all()
    else:
        items = crud_item.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return items

@router.post("/", response_model=ItemResponseSchema)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: ItemSchema,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return crud_item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
