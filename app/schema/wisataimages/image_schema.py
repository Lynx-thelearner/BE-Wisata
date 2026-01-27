from pydantic import BaseModel, Field, EmailStr, StringConstraints, ConfigDict, field_validator, field_serializer
from typing import Optional, Annotated, List
from decimal import Decimal
from datetime import time, datetime
from orm_models import WisataStatus

class WisataImageResponse(BaseModel):
    id_image: int
    id_wisata: int
    image_url: str
    is_primary: bool

    class Config:
        from_attributes = True
