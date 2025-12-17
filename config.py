import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"

    DB_USER = os.environ.get("DB_USER") or "root"
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or "aarohi09"
    DB_HOST = os.environ.get("DB_HOST") or "localhost"
    DB_NAME = os.environ.get("DB_NAME") or "library_system"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

