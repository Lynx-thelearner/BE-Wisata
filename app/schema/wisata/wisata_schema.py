from pydantic import BaseModel, Field, EmailStr, StringConstraints, ConfigDict, field_validator, field_serializer
from typing import Optional, Annotated, List
from decimal import Decimal
from datetime import time, datetime
from orm_models import WisataStatus, Wisata

class WisataBase(BaseModel):
    nama_wisata: str
    deskripsi: str
    lokasi: str
    ticket_price: Optional[Decimal]
    open_time: time
    close_time: time
    
class WisataCreate(WisataBase):
    category_id: int
    facility_id: List[int] = []
    tag_id: List[int] = []
        
class WisataUpdate(BaseModel):
    nama_wisata: Optional[str] = None
    deskripsi: Optional[str] = None
    lokasi: Optional[str] = None
    ticket_price: Optional[Decimal] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    status: Optional[WisataStatus] = None
    category_id: Optional[int] = None
    
class WisataResponse(WisataBase):
    id_wisata: int
    status: WisataStatus
    created_at: datetime
    updated_at: datetime
    category_id: int
    
    @field_serializer("open_time", "close_time")
    def serialize_time(self, value: time):
        return value.strftime("%H:%M")

    facilities: List[str]
    tags: List[str] = Field(default_factory=list)  # <-- default kosong
    images: List[str]

    model_config = ConfigDict(from_attributes=True)

