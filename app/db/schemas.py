from typing import Optional

from pydantic import BaseModel


class Image(BaseModel):
    b64: str


class ImagesResized(BaseModel):
    size32: str
    size64: str


class TaskBase(BaseModel):
    id: str


class TaskInfo(TaskBase):
    status: Optional[str] = None
