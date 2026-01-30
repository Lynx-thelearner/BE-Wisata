from app.core.auth import get_current_user 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from orm_models import UserRole, WisataStatus
from app.core.database import get_db
from app.core.auth import require_role
from app.api.review import review_service
from app.schema.review.review_schema import UserReviewResponse, UserReviewCreate

router = APIRouter(
    prefix="/review",
    tags=["review"]
)
