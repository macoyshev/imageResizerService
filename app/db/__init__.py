from redis import Redis
from rq import Queue

from app.configs import Settings

cache_client = Redis(host=Settings().redis_host, port=Settings().redis_port)

task_queue = Queue(connection=cache_client)
