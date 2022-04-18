from http import HTTPStatus
from typing import Union

from fastapi import APIRouter

from app.db import schemas
from app.services.images import ImageService
from app.services.tasks import TaskService

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=schemas.TaskInfo)
def create_resize_task(image: schemas.Image) -> schemas.TaskInfo:
    task = TaskService.create_task(ImageService.resize, image)

    ImageService.store_in_cache(image, key=task.id)

    return task


@router.get('/{task_id}', response_model=schemas.TaskInfo)
def get_resize_task_status(task_id: str) -> schemas.TaskInfo:
    status = TaskService.get_status(task_id)

    return schemas.TaskInfo(id=task_id, status=status)


@router.get('/{task_id}/image', response_model=schemas.Image)
def get_resize_task_result(task_id: str, size: Union[int, str]) -> schemas.Image:
    resized_image: str = 'image_b64'

    if size == 'original':
        resized_image = ImageService.get_from_cache(task_id).b64

    if size in [32, 64]:
        resized_images = TaskService.get_result(task_id)

        if size == 32:
            resized_image = resized_images.size32

        if size == 64:
            resized_image = resized_images.size64

    return schemas.Image(b64=resized_image)
