from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
from sqlalchemy.orm import Session
from orm_models import UserRole, WisataStatus
from app.core.database import get_db
from app.core.auth import require_role
from app.api.wisata import wisata_service  
from app.schema.wisata.wisata_schema import WisataCreate, WisataUpdate, WisataResponse, ImageResponse

router = APIRouter(
    prefix="/wisata",
    tags=["wisata"]
)

# ======================
# GLOBAL / STATIC ROUTES
# ======================

@router.get("/", response_model=List[WisataResponse],
            dependencies=[Depends(require_role(UserRole.editor, UserRole.admin))])
def get_all_wisata(db: Session = Depends(get_db)):
    return wisata_service.get_all_wisata(db=db)

@router.get("/published", response_model=List[WisataResponse])
def get_published_wisata(db: Session = Depends(get_db)):
    return wisata_service.get_publish_wisata(db=db)

@router.get("/images", response_model=List[ImageResponse])
def get_all_images_endpoint(db: Session = Depends(get_db)):
    return wisata_service.get_all_image(db)

# ======================
# DYNAMIC / ID ROUTES
# ======================

@router.get("/{id_wisata}", response_model=WisataResponse)
def get_wisata_by_id(id_wisata: int, db: Session = Depends(get_db)):
    return wisata_service.get_wisata_by_id(db=db, id_wisata=id_wisata)

@router.post("/", response_model=WisataResponse,
             dependencies=[Depends(require_role(UserRole.editor, UserRole.admin))])
def create_wisata(request: WisataCreate, db: Session = Depends(get_db)):
    return wisata_service.create_wisata(db=db, wisata_data=request)

@router.patch("/{id_wisata}", response_model=WisataResponse,
              dependencies=[Depends(require_role(UserRole.editor, UserRole.admin))])
def update_wisata(id_wisata: int, wisata_data: WisataUpdate, db: Session = Depends(get_db)):
    return wisata_service.update_wisata(
        id_Wisata=id_wisata,
        wisata_data=wisata_data,
        db=db
    )

@router.delete("/{id_wisata}",
               dependencies=[Depends(require_role(UserRole.editor, UserRole.admin))])
def delete_wisata(id_wisata: int, db: Session = Depends(get_db)):
    return wisata_service.delete_wisata(db=db, id_wisata=id_wisata)

# ======================
# IMAGE ACTIONS
# ======================

@router.post("/{id_wisata}/upload-image")
def upload_image(
    id_wisata: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return wisata_service.upload_image(db=db, id_wisata=id_wisata, file=file)

@router.delete("/image/{id_image}")
def delete_image(id_image: int, db: Session = Depends(get_db)):
    return wisata_service.delete_image(db=db, id_image=id_image)
