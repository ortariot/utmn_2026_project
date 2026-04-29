FROM python:3.14 AS base

ENV PYTHONDNTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


FROM base as worker

CMD ["celery", "-A", "celery_app", "worker"]


FROM base as flower

RUN pip install flower

CMD ["celery", "-A", "celery_app", "flower"]
