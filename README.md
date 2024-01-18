# weather_api

## WAY - 1

Load image

```
docker pull semoleg1986/weather-app
```
Start container

```
docker run -p 8000:8000 semoleg1986/weather-app:latest
```

## WAY -2 

## Downloading

```
git clone https://github.com/semoleg1986/weather-api.git
```
## Navigate

```
cd weather-api
```
## Switch to the develop branch

```
git checkout dev
```

## Setting Up Virtual Environment

It's recommended to use a virtual environment. Install pipenv if you haven't already:

```
pip install pipenv
```

Set up a virtual environment and install dependencies:

```
pipenv install
```

Activate the virtual environment:

```
pipenv shell
```

## Running the Application

Run migrations to set up the database:

```
python manage.py migrate
```

Start the Django development server /api/weather?city=<город>:
```
python3 manage.py runserver
```

and other terminal Start the Telegram Bot @Weather-api:
```
python manage.py run_telegram_bot
```

## Running Tests

To run the tests, use the following command:

```
python manage.py test
```

or with coverage:

```
coverage run manage.py test
coverage report
```

| Name                                                     | Stmts | Miss | Cover |
|----------------------------------------------------------|-------|------|-------|
| manage.py                                                | 12    | 2    | 83%   |
| weather/__init__.py                                      | 0     | 0    | 100%  |
| weather/admin.py                                         | 1     | 0    | 100%  |
| weather/apps.py                                          | 4     | 0    | 100%  |
| weather/migrations/0001_initial.py                       | 5     | 0    | 100%  |
| weather/migrations/0002_weather_created_weather_updated.py | 5    | 0    | 100%  |
| weather/migrations/__init__.py                           | 0     | 0    | 100%  |
| weather/models.py                                        | 12    | 1    | 92%   |
| weather/tests.py                                         | 20    | 0    | 100%  |
| weather/urls.py                                          | 3     | 0    | 100%  |
| weather/views.py                                         | 84    | 40   | 52%   |
| weather_api/__init__.py                                   | 0     | 0    | 100%  |
| weather_api/settings.py                                   | 18    | 0    | 100%  |
| weather_api/urls.py                                       | 3     | 0    | 100%  |
| TOTAL                                                    | 167   | 43   | 74%   |
