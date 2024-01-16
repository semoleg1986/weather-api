FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app


COPY Pipfile Pipfile.lock /usr/src/app/

RUN pipenv install --deploy --ignore-pipfile

# Копируем файлы проекта в контейнер
COPY . /usr/src/app/


RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "<your_project_name>.wsgi:application"]