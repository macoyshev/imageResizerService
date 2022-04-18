from typing import Any, Optional

import pytest

from app.db.schemas import Image
from app.errors import InvalidImageSize
from app.services.images import ImageService
from app.services.tasks import TaskService


def function(arg: Optional[Any] = True) -> Optional[Any]:
    return arg


def test_create_task_without(mock_redis_client, mock_redis_task_queue):
    res = TaskService.create_task(function)

    assert res
    assert res.status == 'WAITING'

    mock_redis_client.asserd_called_once()
    mock_redis_task_queue.asserd_called_once()


def test_create_task(mock_redis_client, mock_redis_task_queue):
    res = TaskService.create_task(function)

    assert res
    assert res.status == 'WAITING'

    mock_redis_client.asserd_called_once()
    mock_redis_task_queue.asserd_called_once()


@pytest.mark.parametrize(
    'row_status, expected',
    [
        ('queued', 'WAITING'),
        ('scheduled', 'WAITING'),
        ('deferred', 'WAITING'),
        ('started', 'IN_PROGRESS'),
        ('finished', 'DONE'),
        ('stopped', 'FAILED'),
        ('canceled', 'FAILED'),
        ('failed', 'FAILED'),
    ],
)
def test_convert_status(row_status, expected, mock_redis_client, mock_redis_task_queue):
    assert TaskService.convert_status(row_status) == expected

    mock_redis_client.asserd_called_once()
    mock_redis_task_queue.asserd_called_once()


def test_get_status(mock_redis_client, mock_redis_task_queue):
    task = TaskService.create_task(function)
    res = TaskService.get_status(task.id)

    assert task
    assert res
    assert res == 'WAITING'

    mock_redis_client.asserd_called_once()
    mock_redis_task_queue.asserd_called_once()


def test_resize(image_b64_original):
    image_resized = ImageService.resize(Image(b64=image_b64_original))

    assert image_resized.size32
    assert image_resized.size64


def test_resize_not_square_image_size(image_b64_not_square):
    with pytest.raises(InvalidImageSize):
        ImageService.resize(Image(b64=image_b64_not_square))


def test_b64_to_image(image_b64_original, image_original):
    image = ImageService.b64_to_image(image_b64_original)

    assert image.size == image_original.size


def test_image_to_b64(image_original, image_b64_original):
    image_b64 = ImageService.image_to_b64(image_original)

    assert image_b64_original == image_b64
