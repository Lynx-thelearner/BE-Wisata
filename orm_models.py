from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    Enum,
    DateTime,
    DECIMAL,
    Time,
    CheckConstraint,
    UniqueConstraint,
    SmallInteger,
    Index
    
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from app.core.database import Base


class UserRole(enum.Enum):
    admin = "admin"
    user = "user"
    editor = "editor"
    
class WisataStatus(enum.Enum):
    draft = "draft"
    published = "published"
    
class RecommendationLevel(enum.Enum):
    recommended = "recommended"
    not_recommended = "not_recommended"
    neutral = "neutral"

class User(Base):
    __tablename__ = "users"
    
    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole, name="user_role"), default=UserRole.user, nullable=False) 
    
    editor_reviews = relationship("EditorReview", back_populates="editor")
    user_reviews = relationship("UserReview", back_populates="user")
    
class Wisata(Base):
    __tablename__ = "wisata"
    
    id_wisata = Column(Integer, primary_key=True, index=True)
    nama_wisata = Column(String, nullable=False)
    deskripsi = Column(String, nullable=False)
    lokasi = Column(Text, nullable=False)
    ticket_price = Column(DECIMAL(10, 2), nullable=True)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    
    category_id = Column(
        Integer,
        ForeignKey("categories.id_category"),
        nullable=False
    )
    
    status = Column(Enum(WisataStatus), default=WisataStatus.draft, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    images = relationship("WisataImage", back_populates="wisata")
    editor_reviews = relationship("EditorReview", back_populates="wisata")
    user_reviews = relationship("UserReview", back_populates="wisata")
    tag = relationship("Tag", secondary="wisata_tag", back_populates="wisata")
    facilities = relationship("Facility", secondary="wisata_facilities", back_populates="wisata")
    category = relationship(
        "Category",
        back_populates="wisata"
    )

    
class Category(Base):
    __tablename__ = "categories"
    
    id_category = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    
    wisata = relationship("Wisata", back_populates="category")
class Tag(Base):
    __tablename__ = "tag"
    
    id_tag = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    
    wisata = relationship("Wisata", secondary="wisata_tag", back_populates="tag")
           
class WisataTag(Base):
    __tablename__ = "wisata_tag"

    id_wisata = Column(Integer, ForeignKey(Wisata.id_wisata), nullable=False, primary_key=True)
    id_tag = Column(Integer, ForeignKey(Tag.id_tag), nullable=False, primary_key=True)
    
class Facility(Base):
    __tablename__ = "facilities"
    
    id_facility = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    
    wisata = relationship("Wisata", secondary="wisata_facilities", back_populates="facilities")
    
class WisataFacility(Base):
    __tablename__ = "wisata_facilities"
    
    id_wisata = Column(Integer, ForeignKey(Wisata.id_wisata), nullable=False, primary_key=True)
    id_facility = Column(Integer, ForeignKey(Facility.id_facility), nullable=False, primary_key=True)
    
class WisataImage(Base):
    __tablename__ = "wisata_images"
    
    id_image = Column(Integer, primary_key=True, index=True)
    id_wisata = Column(Integer, ForeignKey(Wisata.id_wisata), nullable=False)
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False,)
    
    __table_args__ = (
        Index(
            "unique_primary_per_wisata",
            "id_wisata",
            unique=True,
            postgresql_where=(is_primary == True) # Hanya berlaku jika is_primary True
        ),
    )
    
    wisata = relationship("Wisata", back_populates="images")
    
class EditorReview(Base):
    __tablename__ = "editor_reviews"
    
    id_review = Column(Integer, primary_key=True, index=True)
    id_wisata = Column(Integer, ForeignKey(Wisata.id_wisata), nullable=False)
    id_editor = Column(Integer, ForeignKey(User.id_user), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    recommendation_level = Column(Enum(RecommendationLevel), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    wisata = relationship("Wisata", back_populates="editor_reviews")
    editor = relationship("User", back_populates="editor_reviews")
    
class UserReview(Base):
    __tablename__ = "user_reviews"
    
    id_review = Column(Integer, primary_key=True, index=True)
    id_wisata = Column(Integer, ForeignKey("wisata.id_wisata"), nullable=False)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)

    rating = Column(SmallInteger, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
    CheckConstraint("rating BETWEEN 1 AND 5"),
    UniqueConstraint("id_wisata", "id_user"),
)


    wisata = relationship("Wisata", back_populates="user_reviews")
    user = relationship("User", back_populates="user_reviews")
    
