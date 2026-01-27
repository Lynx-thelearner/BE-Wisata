from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from orm_models import Tag
from app.core.database import get_db
from app.core.auth import require_role
from app.api.tags import tag_service  
from app.schema.tags.schema import TagsCreate, TagsUpdate, TagsResponse

router = APIRouter(
    prefix="/tag",
    tags=["tag"]
)

@router.get("/", response_model=list[TagsResponse])
def get_all_tags(db: Session = Depends(get_db)):
    return tag_service.get_all_tags(db=db)

@router.get("/{id_tag}", response_model=TagsResponse)
def get_tags_by_id(id_tag:int, db: Session = Depends(get_db)):
    return tag_service.get_tags_by_id(db=db, id_tag=id_tag)

@router.post("/", response_model=TagsResponse)
def create_tags(tags_data:TagsCreate, db: Session = Depends(get_db)):
    return tag_service.create_tags(db=db, tags_data=tags_data)

@router.patch("/{id_tag}", response_model=TagsResponse)
def update_tags(tag_data:TagsUpdate, id_tag:int, db: Session = Depends(get_db)):
    return tag_service.update_tags(db=db, tag_data=tag_data, id_tag=id_tag)

@router.delete("/{id_tag}")
def delete_tags(id_tag:int, db: Session = Depends(get_db)):
    return tag_service.delete_tags(db=db, id_tag=id_tag)