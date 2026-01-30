from pydantic import BaseModel, Field, EmailStr, StringConstraints, ConfigDict, field_validator, field_serializer
from typing import Optional, Annotated, List
from decimal import Decimal
from datetime import time, datetime
from orm_models import WisataStatus

class FacilitiesBase(BaseModel):
    name: str
    
class FacilitiesCreate(FacilitiesBase):
    pass

class FacilitiesUpdate(BaseModel):
    name: Optional[str] = None
    
class FacilitiesResponse(FacilitiesBase):
    id_facility: int
    
    model_config = ConfigDict(
    from_attributes=True
    )