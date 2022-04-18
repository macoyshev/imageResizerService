from http import HTTPStatus


def test_create_resize_task(
    client, image_b64_original, mock_redis_client, mock_redis_task_queue
):
    res = client.post(
        '/tasks/',
        json={
            'b64': image_b64_original,
        },
    )

    task = res.json()

    assert res.status_code == HTTPStatus.CREATED
    assert task
    assert task.get('status') == 'WAITING'

    mock_redis_client.asserd_called_once()
    mock_redis_task_queue.asserd_called_once()


def test_get_resize_task_status(
    client, image_b64_original, mock_redis_client, mock_redis_task_queue
):
    res = client.post('/tasks/', json={'b64': image_b64_original})
    task = res.json()

    res = client.get(f'/tasks/{task.get("id")}')
    task2 = res.json()

    assert task2.get('id') == task.get('id')

    mock_redis_client.asserd_called_once()
    mock_redis_task_queue.asserd_called_once()


def test_get_resize_task_result_image64(
    image_b64_original,
    image_b64_square_64,
    mock_redis_client,
    mock_redis_task_queue,
    client,
):
    res = client.post('/tasks/', json={'b64': image_b64_original})
    task = res.json()

    res = client.get(f'/tasks/{task.get("id")}/image?size=64')
    data = res.json()

    assert res.status_code == HTTPStatus.OK
    assert data.get('b64') == image_b64_square_64

    mock_redis_client.asserd_called_once()
    mock_redis_task_queue.asserd_called_once()


def test_get_resize_task_result_image32(
    image_b64_original,
    image_b64_square_32,
    mock_redis_client,
    mock_redis_task_queue,
    client,
):
    res = client.post('/tasks/', json={'b64': image_b64_original})
    task = res.json()

    res = client.get(f'/tasks/{task.get("id")}/image?size=32')
    data = res.json()

    assert res.status_code == HTTPStatus.OK
    assert data.get('b64') == image_b64_square_32

    mock_redis_client.asserd_called_once()
    mock_redis_task_queue.asserd_called_once()
