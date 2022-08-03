FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
RUN mkdir /code/staticfiles
RUN mkdir /code/mediafiles
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . /code/