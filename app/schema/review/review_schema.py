from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from orm_models import RecommendationLevel

# --- USER REVIEW ---
class UserReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5) # Rating harus 1-5
    comment: Optional[str] = None

class UserReviewCreate(UserReviewBase):
    id_wisata: int

class UserReviewResponse(UserReviewBase):
    id_review: int
    id_user: int
    id_wisata: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
# --- EDITOR REVIEW ---
class EditorReviewBase(BaseModel):
    title: str
    content: str
    recommendation_level: RecommendationLevel
    
class EditorReviewUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    recommendation_level: Optional[RecommendationLevel] = None

class EditorReviewCreate(EditorReviewBase):
    id_wisata: int

class EditorReviewResponse(EditorReviewBase):
    id_review: int
    id_editor: int
    id_wisata: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)