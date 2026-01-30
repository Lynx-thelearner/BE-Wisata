from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from orm_models import Facility
from app.schema.facilities.facilities_schema import FacilitiesCreate, FacilitiesResponse, FacilitiesUpdate
from typing import List, Optional, Dict, Any

def get_all_facility(db: Session) -> List[Facility]:
    return db.query(Facility).all()

def get_facility_by_id(db: Session, id_facility: int) -> Facility | None:
    return db.query(Facility).filter(Facility.id_facility == id_facility).first()

def create_facility(db: Session, facility_data:FacilitiesCreate) -> Facility:
    new_facility = facility_data.model_dump()
    
    facilities = Facility(**new_facility)
    db.add(facilities)
    db.commit()
    db.refresh(facilities)
    return facilities

def update_facility(db: Session, facility_data: FacilitiesUpdate, id_facility: int) -> Facility | None:
    facilities = get_facility_by_id(db=db, id_facility=id_facility)
    if not facilities:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Wisata Tidak Ditemukan")
    update_facilities = facility_data.model_dump(exclude_unset=True)
    
    for key, value in update_facilities.items():
        setattr(facilities, key, value)
        
    db.commit()
    db.refresh(facilities)
    return facilities

def delete_facility(db: Session, id_facility: int) -> Dict[str, str]:
    facilities = db.query(Facility).filter(Facility.id_facility == id_facility).first()
    if not facilities:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="fasilitas tidak ditemukan"
        )
            
    nama = facilities.name
    
    db.delete(facilities)
    db.commit()
    
    return {"status": "success", "message": f"facility {nama} deleted"}