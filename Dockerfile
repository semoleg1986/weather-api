# Use an official Python runtime as a parent image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --ignore-pipfile

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "pipenv run python manage.py runserver 0.0.0.0:8000 & pipenv run python manage.py run_telegram_bot"]


