FROM python:3.12.2-alpine
LABEL maintainer='Grzegorz Zygan'

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG DEV=false

COPY ./search/requirements.txt /tmp/requirements.txt
COPY ./search/requirements.dev.txt /tmp/requirements.dev.txt

COPY ./compose/local/search/start /start
RUN chmod +x /start

COPY ./compose/local/search/cstart /cstart
RUN chmod +x /cstart

COPY ./compose/local/search/fstart /fstart
RUN chmod +x /fstart

COPY ./compose/local/search/bstart /bstart
RUN chmod +x /bstart

COPY ./compose/local/search/entrypoint /entrypoint
RUN chmod +x /entrypoint

RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-libs jpeg-dev && \
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
    search-user

USER search-user

WORKDIR /search

ENTRYPOINT ["/entrypoint"]
