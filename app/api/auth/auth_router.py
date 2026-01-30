from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import auth
from app.core.auth import create_access_token
from app.core.database import get_db
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.user import user_service
from app.api.auth import auth_service
from app.schema.user.user_schema import UserRegis, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=auth.Token)
def login_endpoint(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_service.login_user(db, form_data.username, form_data.password)

