from typing import Any, List, Optional
from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemSchema, ItemUpdateSchema

class CRUDItem:
    def get(self, db: Session, id: Any) -> Optional[Item]:
        return db.query(Item).filter(Item.id == id).first()

    def create_with_owner(
        self, db: Session, *, obj_in: ItemSchema, owner_id: int
    ) -> Item:
        db_obj = Item(**obj_in.dict(), owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (
            db.query(Item)
            .filter(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def remove(self, db: Session, *, id: int) -> Item:
        obj = db.query(Item).get(id)
        db.delete(obj)
        db.commit()
        return obj

item = CRUDItem()
