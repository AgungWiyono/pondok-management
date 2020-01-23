import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "testingkey"
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://postgres:thisisadminspeaking@127.0.0.1/absensi"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    FLASK_ADMIN_SWATCH = "cerulean"
