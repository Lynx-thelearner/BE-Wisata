from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from orm_models import Tag
from app.schema.tags.schema import TagsCreate, TagsResponse, TagsUpdate
from typing import List, Optional, Dict, Any

def get_all_tags(db: Session) -> List[Tag]:
    return db.query(Tag).all()

def get_tags_by_id(db: Session, id_tag: int) -> Tag | None:
    return db.query(Tag).filter(Tag.id_tag == id_tag).first()

def create_tags(db: Session, tags_data:TagsCreate) -> Tag:
    new_tags = tags_data.model_dump()
    
    tags = Tag(**new_tags)
    db.add(tags)
    db.commit()
    db.refresh(tags)
    return tags

def update_tags(db: Session, tag_data: TagsUpdate, id_tag: int) -> Tag | None:
    tags = get_tags_by_id(db=db, id_tag=id_tag)
    if not tags:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Wisata Tidak Ditemukan")
    update_tags = tag_data.model_dump(exclude_unset=True)
    
    for key, value in update_tags.items():
        setattr(tags, key, value)
        
    db.commit()
    db.refresh(tags)
    return tags

def delete_tags(db: Session, id_tag: int) -> Dict[str, str]:
    tags = db.query(Tag).filter(Tag.id_tag == id_tag).first()
    if not tags:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pengguna tidak ditemukan"
        )
            
    nama = tags.name
    
    db.delete(tags)
    db.commit()
    
    return {"status": "success", "message": f"tag {nama} deleted"}