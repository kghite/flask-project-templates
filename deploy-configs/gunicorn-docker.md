0) Testing Gunicorn: `sudo gunicorn -b 0.0.0.0:80 app` 

1) `Dockerfile` in `app` directory

```
FROM python:3.6.7

RUN mkdir -p /home/project/app
WORKDIR /home/project/app
COPY requirements.txt /home/project/app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/project/app
```

2) Test docker container: `docker build --tag app .`, `docker run --detach -p 80:8000 app`

3) `docker-compose.yml` in root directory`

```
version: '3'

services:

  app:
    container_name: app
    restart: always
    build: ./app
    ports:
      - "8000:8000"
    command: gunicorn -w 1 -b :8000 app:server


  nginx:
    container_name: nginx
    restart: always
    build: ./nginx
    ports:
      - "80:80"
    depends_on:
      - app
```

3) Build container: `docker-compose up --build -d`
