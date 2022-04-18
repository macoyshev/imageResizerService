import base64
from io import BytesIO
from typing import Any, Optional
from unittest.mock import MagicMock

import fakeredis
import pytest
import rq
from fastapi.testclient import TestClient
from PIL import Image

from app import create_app
from app.db.schemas import ImagesResized


@pytest.fixture()
def client() -> TestClient:
    test_client = TestClient(create_app())

    return test_client


@pytest.fixture
def function(arg: Optional[Any] = True) -> Optional[Any]:
    return arg


@pytest.fixture
def mock_redis_client(mocker):
    mocked = mocker.patch('app.services.images.cache_client')

    mocked.return_value = fakeredis.FakeStrictRedis()

    return mocked


@pytest.fixture
def mock_redis_task_queue(mocker, fake_task):
    mocked = mocker.patch('app.services.tasks.task_queue')

    mocked.return_value = rq.Queue(connection=fakeredis.FakeStrictRedis)
    mocked.enqueue.return_value = fake_task
    mocked.fetch_job.return_value = fake_task

    return mocked


@pytest.fixture(name='fake_task')
def create_fake_task(image_b64_square_64, image_b64_square_32, image_b64_original):
    mock = MagicMock()

    mock.id = 'fake_task'
    mock.get_status.return_value = 'queued'
    mock.result = ImagesResized(
        size32=image_b64_square_32,
        size64=image_b64_square_64,
        original=image_b64_original,
    )

    return mock


@pytest.fixture(scope='session', name='image_b64_original')
def get_image_b64_original() -> str:
    """
    :return: base64 encoded image of original size
    """
    image = Image.open('tests/app/stuff/test_image.png')
    buffered = BytesIO()
    image.save(buffered, format='JPEG')

    return base64.b64encode(buffered.getvalue()).decode()


@pytest.fixture(scope='session', name='image_b64_square_64')
def get_image_b64_square_64() -> str:
    """
    :return: base64 encoded image of 64x64 size
    """
    image = Image.open('tests/app/stuff/test_image.png')
    image = image.resize((64, 64))
    buffered = BytesIO()
    image.save(buffered, format='JPEG')

    return base64.b64encode(buffered.getvalue()).decode()


@pytest.fixture(scope='session', name='image_b64_square_32')
def get_image_b64_square_32() -> str:
    """
    :return: base64 encoded image of 32x32 size
    """
    image = Image.open('tests/app/stuff/test_image.png')
    image = image.resize((32, 32))
    buffered = BytesIO()
    image.save(buffered, format='JPEG')

    return base64.b64encode(buffered.getvalue()).decode()


@pytest.fixture(scope='session')
def image_b64_not_square() -> str:
    """
    :return: base64 encoded image of 30x32 size
    """
    image = Image.open('tests/app/stuff/test_image.png')
    image = image.resize((30, 32))
    buffered = BytesIO()
    image.save(buffered, format='JPEG')

    return base64.b64encode(buffered.getvalue()).decode()


@pytest.fixture(scope='session')
def image_original() -> Image:
    """
    :return: pillow image of original size
    """
    image = Image.open('tests/app/stuff/test_image.png')

    return image
