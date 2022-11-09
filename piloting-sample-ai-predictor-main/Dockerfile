
FROM python:3.8.12-slim-bullseye
WORKDIR /app

RUN apt-get install   -y
RUN apt-get update && \
   apt-get install -y --no-install-recommends \
       liblapack-dev ffmpeg libsm6 libxext6 libgl1-mesa-glx libatlas-base-dev && \
   rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

CMD ["python", "-u", "main.py"]


