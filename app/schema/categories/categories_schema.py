from pydantic import BaseModel, Field, EmailStr, StringConstraints, ConfigDict, field_validator, field_serializer
from typing import Optional, Annotated, List
from decimal import Decimal
from datetime import time, datetime
from orm_models import WisataStatus

class CategoryBase(BaseModel):
    name: str
    
class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    
class CategoryResponse(CategoryBase):
    id_category: int
    
    model_config = ConfigDict(
    from_attributes=True
    )