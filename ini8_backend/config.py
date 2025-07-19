import os

class Config:
    TESTING = os.getenv("TESTING", "false").lower() == "true"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf'}
    SECRET_KEY = os.getenv("SECRET_KEY", "ini8_secret")
    SQLALCHEMY_DATABASE_URI = (
    "sqlite:///:memory:" if TESTING else
    os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/ini8db"))
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    CACHE_TTL = 30 