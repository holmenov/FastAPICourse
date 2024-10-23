from fastapi import APIRouter, UploadFile

from app.service.images import ImagesService


router = APIRouter(prefix="/images", tags=["Изображения автомобилей"])


@router.post("")
async def upload_image(file: UploadFile):
    await ImagesService().upload_image(file=file)
    return {"success": True}