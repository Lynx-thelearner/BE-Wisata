from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from orm_models import UserRole, WisataStatus
from app.core.database import get_db
from app.core.auth import require_role
from app.api.facilities import facilities_service
from app.schema.facilities.facilities_schema import FacilitiesCreate, FacilitiesResponse, FacilitiesUpdate

router = APIRouter(
    prefix="/facility",
    tags=["facility"]
)

@router.get("/", response_model=list[FacilitiesResponse])
def get_all_facility(db: Session = Depends(get_db)):
    return facilities_service.get_all_facility(db=db)

@router.get("/{id_facility}", response_model=FacilitiesResponse)
def get_facility_by_id(id_facility:int, db: Session = Depends(get_db)):
    return facilities_service.get_facility_by_id(db=db, id_facility=id_facility)

@router.post("/", response_model=FacilitiesResponse)
def create_facility(facility_data:FacilitiesCreate, db: Session = Depends(get_db)):
    return facilities_service.create_facility(db=db, facility_data=facility_data)

@router.patch("/{id_facility}", response_model=FacilitiesResponse)
def update_facility(facility_data:FacilitiesUpdate, id_facility:int, db: Session = Depends(get_db)):
    return facilities_service.update_facility(db=db, facility_data=facility_data, id_facility=id_facility)

@router.delete("/{id_facility}")
def delete_facility(id_facility:int, db: Session = Depends(get_db)):
    return facilities_service.delete_facility(db=db, id_facility=id_facility)