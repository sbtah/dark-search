FROM python:3.13.2-bullseye
LABEL maintainer='Grzegorz Zygan'


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


ARG DEV=false


COPY ./api/requirements.txt /tmp/requirements.txt
COPY ./api/requirements.dev.txt /tmp/requirements.dev.txt

COPY ./compose/local/search/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/search/cstart /cstart
RUN sed -i 's/\r$//g' /cstart
RUN chmod +x /cstart

COPY ./compose/local/search/fstart /fstart
RUN sed -i 's/\r$//g' /fstart
RUN chmod +x /fstart

COPY ./compose/local/search/bstart /bstart
RUN sed -i 's/\r$//g' /bstart
RUN chmod +x /bstart

COPY ./compose/local/search/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


RUN mkdir -p /api/media && \
    mkdir -p /api/static && \
    mkdir -p /api/staticfiles


RUN apt-get update \
  && apt-get install ca-certificates -y \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then pip install -r /tmp/requirements.dev.txt ; \
    fi


WORKDIR /api


ENTRYPOINT ["/entrypoint"]
