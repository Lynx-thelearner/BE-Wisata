from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from orm_models import Wisata, WisataStatus, Tag, Facility, WisataImage
from app.schema.wisata.wisata_schema import WisataCreate, WisataResponse, WisataUpdate
from typing import List, Optional, Dict, Any
import os, shutil
import uuid


def get_all_wisata(db: Session) -> List[Wisata]:
    return db.query(Wisata).order_by(Wisata.id_wisata.asc()).all()


def get_publish_wisata(db: Session) -> List[Wisata]:
    return (
        db.query(Wisata)
        .filter(Wisata.status == WisataStatus.published)
        .order_by(Wisata.id_wisata.desc())
        .all()
    )



def get_wisata_by_id(db: Session, id_wisata: int) -> Wisata | None:
    wisatas = db.query(Wisata).filter(Wisata.id_wisata == id_wisata).first()
    if not wisatas:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wisata tidak ditemukan")

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

    db.commit()
    db.refresh(wisata)
    return wisata


def update_wisata(db: Session, wisata_data: WisataUpdate, id_Wisata: int) -> Wisata | None:
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
    
    #Buat hapus folder gambar
    folder_path = f"app/static/image/wisata{id_wisata}"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path) 

    nama = wisata.nama_wisata

    db.delete(wisata)
    db.commit()

    return {"status": "success", "message": f"Wisata {nama} deleted"}

def get_all_image(db: Session):
    return db.query(WisataImage).all()

def get_image_by_id(db: Session, id_image:int):
    return db.query(WisataImage).filter(WisataImage.id_image == id_image).first()

def upload_image(db: Session, id_wisata: int, file: UploadFile):
    #Cek apakah wisata ada?
    wisata = db.query(Wisata).filter(Wisata.id_wisata == id_wisata).first()
    if not wisata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wisata dengan ID {id_wisata} tidak ditemukan. Tidak bisa upload gambar."
        )

    allowed_types = ["image/jpeg", "image/png", "image/webp"]

    if file.content_type not in allowed_types:
        raise HTTPException(
        status_code=400,
        detail="Format file tidak didukung"
    )

    #Ngecek apakah sudah ada gambar untuk wisata ini?
    existing_images_count = db.query(WisataImage).filter(WisataImage.id_wisata == id_wisata).count()
    
    # Jika belum ada gambar sama sekali, set is_primary jadi True otomatis
    set_as_primary = True if existing_images_count == 0 else False
    #Buat Nentukan dia nyimpan ke folder mana
    base_folder = f"app/static/images/wisata/{id_wisata}"
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        
    #buat bikin nama filenya
    filename = f"{uuid.uuid4()}-{file.filename}"
    file_path = os.path.join(base_folder, filename)
    
    db_path = f"static/images/wisata/{id_wisata}/{filename}"
    
    #Simpan ke storage
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
        
    #simpan path ke supabase
    new_image = WisataImage(id_wisata=id_wisata, image_url=db_path, is_primary=set_as_primary)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    
    return new_image

def delete_image(db: Session, id_image:int):
    image_data = get_image_by_id(db=db, id_image=id_image)
    
    if not image_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tidak menemukan gambar")
    
    file_path = image_data.image_url
    
    if not file_path.startswith("app/"):
        full_path = f"app/{file_path}"
    else:
        full_path = file_path 
        
    next_image = None

    if image_data.is_primary:
        image_data.is_primary = False

    next_image = (
        db.query(WisataImage)
        .filter(
            WisataImage.id_wisata == image_data.id_wisata,
            WisataImage.id_image != image_data.id_image
        )
        .order_by(WisataImage.id_image.asc())
        .first()
    )

    if next_image:
        next_image.is_primary = True



        
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
    except Exception as e:
        print(f"gagal menghapus file di server: {e}")
        
    db.delete(image_data)
    db.commit()

    return {"status": "success", "message": "Gambar berhasil dihapus selamanya."}