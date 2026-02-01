from pydantic import BaseModel, Field, EmailStr, StringConstraints, ConfigDict, field_validator, field_serializer, model_validator
from typing import Optional, Annotated, List, Any
from decimal import Decimal
from datetime import time, datetime
from orm_models import WisataStatus, Wisata, Tag

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
    facility_id: Optional[List[int]] = None
    tag_id: Optional[List[int]] = None
    
class WisataResponse(WisataBase):
    id_wisata: int
    status: WisataStatus
    created_at: datetime
    updated_at: datetime
    category_id: int
    
    facilities: List[Any] = Field(default_factory=list)
    tag: List[Any] = Field(default_factory=list)
    images: List[Any] = Field(default_factory=list) # Tambahkan default factory biar aman kalau kosong
    image_cover: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    @model_validator(mode="after")
    def set_image_cover(self) -> "WisataResponse":
        # self.images di sini sudah diproses
        # Kita cari yang primary
        if self.images:
            # Jika images berisi object ORM (saat awal dari DB)
            for img in self.images:
                # Cek atribut .is_primary dari object WisataImage
                if getattr(img, 'is_primary', False):
                    self.image_cover = getattr(img, 'image_url', None)
                    break
            
            # Jika tidak ada yang primary, ambil gambar pertama sebagai cadangan
            if not self.image_cover and len(self.images) > 0:
                self.image_cover = getattr(self.images[0], 'image_url', None)
        
        return self
    
    @field_serializer("open_time", "close_time")
    def serialize_time(self, value: time):
        return value.strftime("%H:%M")
    
    @field_serializer("facilities")
    def serialize_facilities(self, value):
        # value adalah list object SQLAlchemy. Kita ambil namanya saja.
        return [f.name for f in value]

    @field_serializer("tag")
    def serialize_tags(self, value):
        return [t.name for t in value]
        
    # Kamu mungkin perlu serializer untuk images juga jika di DB bentuknya Object
    @field_serializer("images")
    def serialize_images(self, value):
        # Asumsi: value adalah list object Image, dan punya atribut 'image_url'
        # Jika value sudah string (karena logic lain), serializer ini opsional
        try:
            return [img.image_url for img in value]
        except AttributeError:
            return value

class ImageResponse(BaseModel):
    id_image: int
    id_wisata: int
    image_url: str
    is_primary: bool

    model_config = ConfigDict(from_attributes=True)