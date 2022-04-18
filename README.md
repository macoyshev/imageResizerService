# imageResizer

### Description:
Api service for resize image. 
There are two ways to run the app,
the first one is to execute [up](#run-app), 
[redis](#run-redis), and [worker](#run-worker)
commands and the second is to [run containers](#run-containers).
For image resizing, 
send a `POST` request on `/tasks` 
and in the body provide an image in
base64 or execute command 
`curl -v  POST 127.0.0.1:8000/tasks/ 
-H "Content-Type: application/json" 
-d '{"b64": "your base64 image"}`. 
The server will send a JSON 
answer with the task id inside.
Use this id to check status, 
for that send `GET` request on 
`/task/{task-id}` if task is done, send `GET` request 
on `/tasks/{task-id}/image` with the required 
size param to get the result 
of resizing in base64. Launch the application 
and go to `127.0.0.1:8000/docs`
to see full api documentation.
### Create venv:
    make venv

### Run app
    make up

### Run redis
    make redis

### Run worker
    make worker

### Create containers
    docker-compose build

### Run containers
    docker-compose up -d

### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format


