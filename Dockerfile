FROM python:3.9-alpine3.13
LABEL maintainer="xavier_nhagumbe@echomoz.org"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app /app
# COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client  mariadb-connector-c && \
    apk add --update --no-cache --virtual .tmp-deps gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev \
    # apk add --update --no-cache postgresql-client && \
    # apk add --update --no-cache --virtual .tmp-deps \
    build-base postgresql-dev musl-dev linux-headers mariadb-dev && \
    # build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    mkdir -p /certificate && \
    chown -R app:app /vol && \
    chmod -R 755 /vol/web && \
    chown -R app:app /certificate && \
    chmod -R 755 /certificate && \
    chmod -R 777 /py/*
# chmod -R +x /scripts

# ENV PATH="/scripts:/py/bin:$PATH"
ENV PATH="/py/bin:$PATH"

USER app