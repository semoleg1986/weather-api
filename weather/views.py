from django.http import JsonResponse
from django.views import View
import requests
from geopy.geocoders import Nominatim
from translate import Translator
from .models import Weather
from decouple import config

class WeatherAPIView(View):
    def get(self, request):
        city_name = request.GET.get('city')
        latitude, longitude = self.get_coordinates(city_name)
        weather_data = self.get_weather_data(latitude, longitude, city_name)
        return JsonResponse(weather_data)

    def get_coordinates(self, city_name):
        geolocator = Nominatim(user_agent="weather_app")
        try:
            location = geolocator.geocode(city_name)
            if location:
                return location.latitude, location.longitude
        except Exception as e:
            pass

        return None, None

    def translate_city_name(self, city_name, target_language='en'):
        translator = Translator(to_lang=target_language)
        return translator.translate(city_name)


    def get_weather_data(self, latitude, longitude, city_name):
            if latitude is None or longitude is None:
                return {'error': 'Coordinates not found for the specified city.'}

            translated_city_name = self.translate_city_name(city_name)
            weather_record = Weather.objects.filter(latitude=latitude, longitude=longitude, city=translated_city_name).first()

            if weather_record:
                return {
                    'temperature': weather_record.temperature,
                    'pressure': weather_record.pressure,
                    'wind_speed': weather_record.wind_speed,
                }
            else:
                yandex_api_url = f"https://api.weather.yandex.ru/v2/informers?lat={latitude}&lon={longitude}"
                yandex_api_key = config('YANDEX_API_KEY')
                headers = {"X-Yandex-API-Key": yandex_api_key}

                try:
                    response = requests.get(yandex_api_url, headers=headers)
                    response.raise_for_status()

                    yandex_data = response.json()['fact']

                    Weather.objects.create(
                        latitude=latitude,
                        longitude=longitude,
                        city=translated_city_name,
                        temperature=yandex_data['temp'],
                        pressure=yandex_data['pressure_mm'],
                        wind_speed=yandex_data['wind_speed'],
                    )

                    return {
                        'temperature': yandex_data['temp'],
                        'pressure': yandex_data['pressure_mm'],
                        'wind_speed': yandex_data['wind_speed'],
                    }
                except requests.RequestException as e:
                    return {
                        'error': f"Failed to fetch data from Yandex API: {str(e)}",
                    }