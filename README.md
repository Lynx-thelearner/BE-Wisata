# Borneo - Sistem Informasi Wisata Kaltim

Aplikasi backend untuk platform informasi pariwisata alam Kalimantan Timur yang dibangun menggunakan FastAPI dan SQLAlchemy.

##  Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Struktur Proyek](#struktur-proyek)
- [Instalasi](#instalasi)
- [Konfigurasi](#konfigurasi)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [API Endpoints](#api-endpoints)
- [Database](#database)
- [Kontribusi](#kontribusi)

##  Fitur Utama

- **Manajemen Wisata**: CRUD untuk destinasi wisata alam
- **Sistem Kategori**: Kategorisasi destinasi wisata
- **Fasilitas**: Kelola fasilitas di setiap destinasi
- **Tag/Label**: Penandaan wisata dengan tag
- **Ulasan & Rating**: Sistem review dan rating untuk wisata
- **Manajemen User**: Registrasi, login, dan manajemen profil pengguna
- **Sistem Gambar**: Upload dan manajemen foto wisata
- **Autentikasi**: Keamanan dengan JWT token
- **CORS Enabled**: Support untuk akses lintas domain

##  Teknologi yang Digunakan

- **Framework**: FastAPI 0.121.0+
- **Database**: PostgreSQL dengan SQLAlchemy ORM
- **Autentikasi**: JWT dengan python-jose
- **Password Hashing**: bcrypt dan passlib
- **Database Migration**: Alembic
- **Server**: Uvicorn (built-in dengan FastAPI)
- **Async Database**: asyncpg
- **Testing**: pytest dan pytest-asyncio
- **Python Version**: 3.13+

##  Struktur Proyek

```
wisata-alam/
├── app/
│   ├── api/                      # Router dan service API
│   │   ├── __init__.py
│   │   ├── auth/                # Autentikasi
│   │   │   ├── auth_router.py
│   │   │   └── auth_service.py
│   │   ├── user/                # Manajemen user
│   │   │   ├── user_router.py
│   │   │   └── user_service.py
│   │   ├── wisata/              # Data wisata
│   │   │   ├── wisata_router.py
│   │   │   └── wisata_service.py
│   │   ├── category/            # Kategori wisata
│   │   │   ├── category_router.py
│   │   │   └── category_service.py
│   │   ├── facilities/          # Fasilitas
│   │   │   ├── facility_router.py
│   │   │   └── facilities_service.py
│   │   ├── tags/                # Tag/Label
│   │   │   ├── tags_router.py
│   │   │   └── tag_service.py
│   │   ├── review/              # Review dan rating
│   │       ├── review_router.py
│   │       └── review_service.py
│   │   
│   ├── core/                     # Konfigurasi inti
│   │   ├── auth.py              # Logika autentikasi
│   │   ├── database.py          # Koneksi database
│   │   └── security.py          # Fungsi keamanan
│   ├── schema/                   # Pydantic models
│   │   ├── user/
│   │   │   └── user_schema.py
│   │   ├── wisata/
│   │   │   └── wisata_schema.py
│   │   ├── categories/
│   │   │   └── categories_schema.py
│   │   ├── facilities/
│   │   │   └── facilities_schema.py
│   │   ├── tags/
│   │   │   └── schema.py
│   │   ├── review/
│   │   │   └── review_schema.py
│   │   └── wisataimages/
│   │       └── image_schema.py
│   └── static/                   # File statis
│       └── images/
│           └── wisata/          # Folder gambar per wisata ID
│               ├── 4/
│               ├── 8/
│               ├── 13/
│               └── 14/
├── alembic/                      # Database migrations
│   └── versions/                # Versi migration
├── main.py                       # Entry point aplikasi
├── orm_models.py                # SQLAlchemy models
├── pyproject.toml               # Konfigurasi project
├── alembic.ini                  # Konfigurasi Alembic
└── README.md                    # File ini
```

##  Instalasi

### Prerequisites
- Python 3.11+ (Dites pada Python 3.13)
- PostgreSQL 12 atau lebih tinggi
- [uv](https://docs.astral.sh/uv/) (Package installer yang cepat untuk Python)

### Langkah-langkah

1. **Clone Repository**
   ```bash
   git clone https://github.com/Lynx-thelearner/BE-Wisata.git
   cd BE-Wisata
   ```

2. **Buat Virtual Environment dan Install Dependencies**
   ```bash
   uv sync
   ```
   
   Atau jika ingin membuat environment dengan Python version tertentu:
   ```bash
   uv sync --python 3.13
   ```

3. **Aktifkan Virtual Environment** (opsional, uv otomatis mengaktifkan)
   ```bash
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

4. **Setup Environment Variables**
   Buat file `.env` di root directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost/wisata_db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Setup Database**
   ```bash
   # Membuat database di PostgreSQL
   createdb wisata_db
   
   # Jalankan migration
   alembic upgrade head
   ```

### Perintah-perintah uv yang Berguna

```bash
# Install dependencies dari pyproject.toml
uv sync

# Menjalankan script dengan uv
uv run main.py

# Menjalankan uvicorn
uv run uvicorn main:app --reload

# Menjalankan fastapi dev
uv run fastapi dev main.py

# Menambah dependency baru
uv add package-name

# Menambah dependency dev
uv add --dev package-name

# Menghapus dependency
uv remove package-name

# Update semua dependencies
uv sync --upgrade
```

##  Konfigurasi

### Database
Edit `app/core/database.py` untuk mengubah konfigurasi database:
```python
DATABASE_URL = "postgresql://username:password@localhost/wisata_db"
```

### JWT Secret
Ubah `SECRET_KEY` di `app/core/security.py` dengan secret key yang aman.

### CORS
Untuk membatasi akses, ubah konfigurasi CORS di `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Ganti dengan URL frontend Anda
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

##  Menjalankan Aplikasi

### Uvicorn
``` bash
uv run uvicorn main:app --reload
```

### Development Mode
```bash
fastapi dev main.py
```
Aplikasi akan berjalan di `http://localhost:8000`

### Production Mode
```bash
fastapi run main.py --host 0.0.0.0 --port 8000
```

### Akses API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - Registrasi user baru
- `POST /auth/login` - Login user

### User
- `GET /users/me` - Get profil user yang login
- `PUT /users/{id}` - Update profil user
- `GET /users/{id}` - Get detail user

### Wisata
- `GET /wisata` - Daftar semua wisata
- `GET /wisata/published` - Daftar wisata yang dipublikasikan
- `GET /wisata/{id}` - Detail wisata berdasarkan ID
- `POST /wisata` - Tambah wisata baru
- `PATCH /wisata/{id}` - Update wisata
- `DELETE /wisata/{id}` - Hapus wisata
- `POST /wisata/{id}/upload-image` - Upload gambar untuk wisata
- `DELETE /wisata/image/{id}` - Hapus gambar wisata
- `GET /wisata/images` - Daftar semua gambar wisata

### Kategori
- `GET /categories` - Daftar kategori
- `POST /categories` - Tambah kategori
- `PUT /categories/{id}` - Update kategori
- `DELETE /categories/{id}` - Hapus kategori

### Fasilitas
- `GET /facilities` - Daftar fasilitas
- `POST /facilities` - Tambah fasilitas
- `PUT /facilities/{id}` - Update fasilitas
- `DELETE /facilities/{id}` - Hapus fasilitas

### Tag
- `GET /tags` - Daftar tag
- `POST /tags` - Tambah tag
- `PUT /tags/{id}` - Update tag
- `DELETE /tags/{id}` - Hapus tag

### Review
- `GET /reviews/{wisata_id}` - Review untuk wisata
- `POST /reviews` - Tambah review
- `PUT /reviews/{id}` - Update review
- `DELETE /reviews/{id}` - Hapus review

### Images
**Catatan**: Endpoint gambar terintegrasi dalam wisata router
- Upload gambar dilakukan melalui: `POST /wisata/{id}/upload-image`
- Hapus gambar dilakukan melalui: `DELETE /wisata/image/{id}`
- Gambar disimpan di: `/app/static/images/wisata/{wisata_id}/`

##  Database

### ORM Models
Semua model database didefinisikan di `orm_models.py` menggunakan SQLAlchemy.

### Migrations
Kelola database schema dengan Alembic:

```bash
# Membuat migration baru
alembic revision --autogenerate -m "Deskripsi perubahan"

# Menjalankan migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

##  Testing

Jalankan test suite:
```bash
pytest
```

Dengan coverage:
```bash
pytest --cov=app
```

##  Kontribusi

Kontribusi diterima! Silakan:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📧 Kontak

Untuk pertanyaan atau saran, silakan hubungi melalui GitHub Issues.

---

**Dibangun oleh Lynx-thelearner**
