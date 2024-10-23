import shutil
from fastapi import UploadFile

from app.service.base import BaseService
from app.tasks.tasks import resize_image


class ImagesService(BaseService):
    def upload_image(self, file: UploadFile):
        image_path = f"app/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)
    
        resize_image.delay(image_path)