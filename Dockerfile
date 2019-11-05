FROM python:latest
ENV PYTHONUNBUFFERED 1
ADD . /srv/app
WORKDIR /srv/app
RUN pip install -r requirements.txt

