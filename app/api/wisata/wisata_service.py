from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from orm_models import Wisata, WisataStatus, Tag, Facility
from app.schema.wisata.wisata_schema import WisataCreate, WisataResponse, WisataUpdate
from typing import List, Optional, Dict, Any


def get_all_wisata(db: Session) -> List[Wisata]:
    wisatas = db.query(Wisata).all()
    for w in wisatas:
        # mapping tags ke list[str]
        w.tags = [t.name for t in w.tag]
        # mapping facilities sama images juga bisa
        w.facilities = [f.name for f in w.facilities]
        w.images = [img.image_url for img in w.images]
    return wisatas


def get_publish_wisata(db: Session) -> List[Wisata]:
    return db.query(Wisata).filter(Wisata.status == WisataStatus.published).all()


def get_wisata_by_id(db: Session, id_wisata: int) -> Wisata | None:
    wisatas = db.query(Wisata).filter(Wisata.id_wisata == id_wisata).first()
    if not wisatas:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wisata tidak ditemukan")

    # mapping ke list[str] langsung
    wisatas.tags = [t.name for t in wisatas.tag]
    wisatas.facilities = [f.name for f in wisatas.facilities]
    wisatas.images = [img.image_url for img in wisatas.images]
    return wisatas


def create_wisata(db: Session, wisata_data: WisataCreate) -> Wisata:
    data = wisata_data.model_dump()

    facility_ids = data.pop("facility_id", [])
    tag_ids = data.pop("tag_id", [])

    wisata = Wisata(**data)
    db.add(wisata)
    db.flush()

    if facility_ids:
        wisata.facilities = (
            db.query(Facility).filter(Facility.id_facility.in_(facility_ids)).all()
        )

    if tag_ids:
        wisata.tag = db.query(Tag).filter(Tag.id_tag.in_(tag_ids)).all()

    wisata.tags = [t.name for t in wisata.tag]  # mapping ORM -> list[str]

    db.commit()
    db.refresh(wisata)
    return wisata


def update_wisata(
    db: Session, wisata_data: WisataUpdate, id_Wisata: int
) -> Wisata | None:
    wisata = get_wisata_by_id(db=db, id_wisata=id_Wisata)
    if not wisata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wisata Tidak Ditemukan"
        )
    update_wisata = wisata_data.model_dump(exclude_unset=True)
    
    if "category_id" in update_wisata:
        wisata.category_id = update_wisata.pop("category_id")


    if "tag_id" in update_wisata:
        tag_ids = update_wisata.pop("tag_id")
    wisata.tag = db.query(Tag).filter(Tag.id_tag.in_(tag_ids)).all()
    wisata.tags = [t.name for t in wisata.tag]  # mapping ke list[str]


    if "facility_id" in update_wisata:
        facility_ids = update_wisata.pop("facility_id")
    wisata.facilities = (
        db.query(Facility).filter(Facility.id_facility.in_(facility_ids)).all()
    )

    for key, value in update_wisata.items():
        setattr(wisata, key, value)

    db.commit()
    db.refresh(wisata)
    return wisata


def delete_wisata(db: Session, id_wisata: int) -> Dict[str, str]:
    wisata = db.query(Wisata).filter(Wisata.id_wisata == id_wisata).first()
    if not wisata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wisata tidak ditemukan"
        )

    nama = wisata.nama_wisata

    db.delete(wisata)
    db.commit()

    return {"status": "success", "message": f"Wisata {nama} deleted"}
