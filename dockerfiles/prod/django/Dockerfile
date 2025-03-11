# pull official base image
FROM python:3.10-slim-buster

# maintainers info
LABEL maintainer="bigdeli.ali3@gmail.com"


# install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


# ایجاد کاربر با UID 1000 (فقط اگر وجود نداشته باشد)
RUN if ! id -u 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 myuser && \
        useradd -u 1000 -g myuser -m -s /bin/bash myuser; \
    fi


# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY ./core .

# collecting static files
CMD python3 manage.py collectstatic --no-input
