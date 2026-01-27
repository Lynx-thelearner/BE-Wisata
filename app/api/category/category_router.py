from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from orm_models import UserRole, WisataStatus
from app.core.database import get_db
from app.core.auth import require_role
from app.api.category import category_service  
from app.schema.categories.categories_schema import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(
    prefix="/category",
    tags=["category"]
)

@router.get("/", response_model=list[CategoryResponse])
def get_all_category(db: Session = Depends(get_db)):
    return category_service.get_all_category(db=db)

@router.get("/{id_category}", response_model=CategoryResponse)
def get_category_by_id(id_category:int, db: Session = Depends(get_db)):
    return category_service.get_category_by_id(db=db, id_category=id_category)

@router.post("/", response_model=CategoryResponse)
def create_category(category_data:CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db=db, category_data=category_data)

@router.patch("/{id_category}", response_model=CategoryResponse)
def update_category(category_data:CategoryUpdate, id_category:int, db: Session = Depends(get_db)):
    return category_service.update_category(db=db, category_data=category_data, id_category=id_category)

@router.delete("/{id_category}")
def delete_category(id_category:int, db: Session = Depends(get_db)):
    return category_service.delete_category(db=db, id_category=id_category)