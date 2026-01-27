from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from orm_models import Category
from app.schema.categories.categories_schema import CategoryCreate, CategoryResponse, CategoryUpdate
from typing import List, Optional, Dict, Any

def get_all_category(db: Session) -> List[Category]:
    return db.query(Category).all()

def get_category_by_id(db: Session, id_category: int) -> Category:
    return db.query(Category).filter(Category.id_category == id_category).first()

def create_category(db: Session, category_data:CategoryCreate) -> Category:
    new_category = category_data.model_dump()
    
    category = Category(**new_category)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def update_category(db: Session, category_data: CategoryUpdate, id_category: int) -> Category | None:
    category = get_category_by_id(db=db, id_category=id_category)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Category Tidak Ditemukan")
    update_category = category_data.model_dump(exclude_unset=True)
    
    for key, value in update_category.items():
        setattr(category, key, value)
        
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, id_category: int) -> Dict[str, str]:
    category = db.query(Category).filter(Category.id_category == id_category).first()
    if not category:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category tidak ditemukan"
        )
            
    nama = category.name
    
    db.delete(category)
    db.commit()
    
    return {"status": "success", "message": f"Category {nama} deleted"}