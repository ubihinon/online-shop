FROM python:3.6

RUN mkdir /app;
RUN cd app
RUN mkdir /src;
WORKDIR /src

COPY /config/requirements.txt /app
COPY /wait_for_postgres.py /app
COPY /config/django-entrypoint.sh /app/src
COPY /config/run_celery.sh /app/src
COPY /fixtures/ /app/src

RUN pip install -r /app/requirements.txt --no-cache-dir

RUN adduser --disabled-password --gecos '' online_shop
