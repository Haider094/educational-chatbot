import os
class Config:
    DEBUG = os.getenv("DEBUG", False)
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    MODEL_PATH = os.getenv("MODEL_PATH", "./model_files/finetuned_model/")
    OFFLOAD_FOLDER = os.getenv("OFFLOAD_FOLDER", "./OffloadFolder")
