from pydantic import BaseModel, Field, EmailStr, StringConstraints, ConfigDict, field_validator, field_serializer
from typing import Optional, Annotated, List
from decimal import Decimal
from datetime import time, datetime
from orm_models import WisataStatus

class TagsBase(BaseModel):
    name: str
    
class TagsCreate(TagsBase):
    pass

class TagsUpdate(BaseModel):
    name: Optional[str] = None
    
class TagsResponse(TagsBase):
    id_tag: int
    
    model_config = ConfigDict(
    from_attributes=True
    )