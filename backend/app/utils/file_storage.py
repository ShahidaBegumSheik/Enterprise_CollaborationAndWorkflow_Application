import os
import uuid
import shutil
from fastapi import UploadFile
from app.core.config import settings

def save_upload(file: UploadFile) -> tuple[str, str]:
    os.makedirs(settings.upload_dir, exist_ok=True)

    extension = file.filename.split(".")[-1] if file.filename and "." in file.filename else "bin"
    stored_name = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(settings.upload_dir, stored_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return stored_name, file_path

