FROM python:3.11.4-alpine
LABEL maintainer='Grzegorz Zygan'

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG DEV=false

COPY ./scout/requirements.txt /tmp/requirements.txt
COPY ./scout/requirements.dev.txt /tmp/requirements.dev.txt


COPY ./compose/local/scout/start /start
RUN chmod +x /start

COPY ./compose/local/scout/cstart /cstart
RUN chmod +x /cstart

COPY ./compose/local/scout/fstart /fstart
RUN chmod +x /fstart

COPY ./compose/local/scout/bstart /bstart
RUN chmod +x /bstart

COPY ./compose/local/scout/entrypoint /entrypoint
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
    scout-user

USER scout-user

WORKDIR /scout

ENTRYPOINT ["/entrypoint"]