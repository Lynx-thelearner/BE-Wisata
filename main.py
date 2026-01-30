import orm_models
from app.core.database import engine
orm_models.Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import Session
from fastapi import FastAPI
from app.api import routers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

""""Inisialisasi aplikasi"""
app = FastAPI(
    title="Borneo",
    description="Sistem informasi wisata Kaltim",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Masukin Router"""
for r in routers:
    app.include_router(r)

"""Awal halaman"""
@app.get("/")
def root():
    return {"message": "This is Borneo"}
