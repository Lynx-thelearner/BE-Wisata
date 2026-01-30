from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from orm_models import UserReview, EditorReview, Wisata
from app.schema.review.review_schema import (
    EditorReviewCreate,
    EditorReviewResponse,
    EditorReviewUpdate,
    UserReviewCreate,
    UserReviewResponse,
)



def create_user_review(db: Session, review_data:UserReviewCreate, id_user:int):
    wisata = db.query(Wisata).filter(Wisata.id_wisata == review_data.id_wisata).first()
    
    if not wisata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tempat wisata tidak ditemukan")
    
    existing_review = (db.query(UserReview).filter(UserReview.id_wisata == review_data.id_wisata,
                                                   UserReview.id_user == id_user))
    
    if existing_review:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Kamu sudah pernah membuat review di wisata ini, Silahkan update reviewmu saja")
    
    new_review = UserReview(
        id_wisata=review_data.id_wisata,
        id_user=id_user,
        rating=review_data.rating,
        comment=review_data.comment
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    return new_review

def create_editor_review(db: Session, review_data: EditorReviewCreate, editor_id: int):
    new_review = EditorReview(**review_data.model_dump(), id_editor=editor_id)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review
