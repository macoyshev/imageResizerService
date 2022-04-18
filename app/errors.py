from fastapi.exceptions import HTTPException


class InvalidImageSize(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail='Invalid image size')


class TaskNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail='Task not found')


class ImageNotCached(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail='Image was not in cache')
