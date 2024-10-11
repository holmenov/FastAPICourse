import os
from PIL import Image

from app.tasks.celery_app import celery_instance


@celery_instance.task
def resize_image(image_path: str):
    sizes = [1000, 500, 200]
    output_folder = "app/static/images"

    img = Image.open(image_path)
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        resized_img = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)
        new_file_name = f"{name}_{size}px{ext}"
        output_path = os.path.join(output_folder, new_file_name)
        resized_img.save(output_path)