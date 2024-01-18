import requests
from decouple import config

class YandexWeatherAPI:
    @staticmethod
    def get_weather_data(latitude, longitude):
        yandex_api_url = f"https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}"
        yandex_api_key = config('YANDEX_API_KEY')
        headers = {"X-Yandex-API-Key": yandex_api_key}

        try:
            response = requests.get(yandex_api_url, headers=headers)
            response.raise_for_status()

            yandex_data = response.json()['fact']
            return {
                'temperature': yandex_data['temp'],
                'pressure': yandex_data['pressure_mm'],
                'wind_speed': yandex_data['wind_speed'],
            }
        except requests.RequestException as e:
            return {
                'error': f"Failed to fetch data from Yandex API: {str(e)}",
            }
