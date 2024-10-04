import os
class Config:
    DEBUG = os.getenv("DEBUG", False)
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    OFFLOAD_FOLDER = os.getenv("OFFLOAD_FOLDER", "./OffloadFolder")
