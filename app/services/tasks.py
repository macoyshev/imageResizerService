from typing import Any, Callable

from app.db import task_queue
from app.db.schemas import TaskInfo
from app.errors import TaskNotFound


class TaskService:
    @staticmethod
    def create_task(func: Callable[..., Any], *args: Any, **kwargs: Any) -> TaskInfo:
        job = task_queue.enqueue(func, args=args, kwargs=kwargs, result_ttl=30)

        return TaskInfo(id=job.id, status=TaskService.convert_status(job.get_status()))

    @staticmethod
    def convert_status(status: str) -> str:
        if status in ['queued', 'scheduled', 'deferred']:
            status = 'WAITING'

        if status in ['started']:
            status = 'IN_PROGRESS'

        if status in ['finished']:
            status = 'DONE'

        if status in ['stopped', 'canceled', 'failed']:
            status = 'FAILED'

        return status

    @staticmethod
    def get_status(task_id: str) -> str:
        job = task_queue.fetch_job(task_id)

        if not job:
            raise TaskNotFound()

        job_status = TaskService.convert_status(job.get_status())

        return job_status

    @staticmethod
    def get_result(task_id: str) -> Any:
        job = task_queue.fetch_job(task_id)

        if not job:
            raise TaskNotFound()

        return job.result
