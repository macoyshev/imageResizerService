import base64
import pickle
from io import BytesIO

from PIL import Image

from app.db import cache_client, schemas
from app.errors import ImageNotCached, InvalidImageSize


class ImageService:
    @staticmethod
    def resize(row_image: schemas.Image) -> schemas.ImagesResized:
        image = Image.open(BytesIO(base64.b64decode(row_image.b64)))

        image_width, image_height = image.size

        if image_width != image_height:
            raise InvalidImageSize()

        image_resized64 = image.resize((64, 64))
        image_resized32 = image.resize((32, 32))

        return schemas.ImagesResized(
            size64=ImageService.image_to_b64(image_resized64),
            size32=ImageService.image_to_b64(image_resized32),
        )

    @staticmethod
    def store_in_cache(image: schemas.Image, key: str) -> None:
        cache_client.set(key, pickle.dumps(image))

    @staticmethod
    def get_from_cache(key: str) -> schemas.Image:
        res = cache_client.get(key)

        if not res:
            raise ImageNotCached()

        image = pickle.loads(res)

        return schemas.Image(b64=image.b64)

    @staticmethod
    def b64_to_image(image_b64: str) -> Image:
        image = Image.open(BytesIO(base64.b64decode(image_b64)))

        return image

    @staticmethod
    def image_to_b64(image: Image) -> str:
        image_file = BytesIO()

        image.save(image_file, format='JPEG')

        image_b64 = base64.b64encode(image_file.getvalue())

        return image_b64.decode()
