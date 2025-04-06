FROM python:3.12.4-alpine
LABEL maintainer='Grzegorz Zygan'

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG DEV=false

COPY ./api/requirements.txt /tmp/requirements.txt
COPY ./api/requirements.dev.txt /tmp/requirements.dev.txt


COPY ./compose/local/api/start /start
RUN chmod +x /start

COPY ./compose/local/api/cstart /cstart
RUN chmod +x /cstart

COPY ./compose/local/api/fstart /fstart
RUN chmod +x /fstart

COPY ./compose/local/api/bstart /bstart
RUN chmod +x /bstart

COPY ./compose/local/api/entrypoint /entrypoint
RUN chmod +x /entrypoint

RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
    --disabled-password \
    --no-create-home \
    api-user && \
    mkdir -p /api/media && \
    mkdir -p /api/static && \
    mkdir -p /api/staticfiles && \
    chown -R api-user:api-user /api && \
    chmod -R 644 /api

USER api-user

WORKDIR /api

ENTRYPOINT ["/entrypoint"]
