# FROM python:3
FROM python:3.9.13
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y build-essential libzbar-dev
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY ./services /app/services
COPY ./src /app/src
COPY ./data /app/data
WORKDIR /app
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5001", "services:create_app()"]
