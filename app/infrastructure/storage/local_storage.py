import os
from .base import StorageInterface

class LocalStorage(StorageInterface):
    upload_DIR = "uploads"

    async def save(self, file, filename: str) -> str:
        os.makedirs(self.upload_DIR, exist_ok=True)
        path = f"{self.upload_DIR}/{filename}"

        with open(path, "wb") as f:
            f.write(await file.read())

        return path
