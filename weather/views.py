from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Weather
from rest_framework import status
import requests
from geopy.geocoders import Nominatim
from translate import Translator
from decouple import config
from datetime import datetime, timedelta
from django.utils import timezone
from .weather_api import YandexWeatherAPI

class WeatherAPIView(APIView):
    def get(self, request):
        city_name = request.GET.get('city')
        latitude, longitude = self.get_coordinates(city_name.lower())
        weather_data = self.get_weather_data(latitude, longitude, city_name)
        return Response(weather_data)

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
        translator = Translator(from_lang="ru", to_lang=target_language)
        translated_name = translator.translate(city_name)
        return translated_name.lower()

    def get_weather_data(self, latitude, longitude, city_name):
            if latitude is None or longitude is None:
                return {'error': 'Coordinates not found for the specified city.'}

            translated_city_name = self.translate_city_name(city_name)
            weather_record = Weather.objects.filter(city=translated_city_name).first()

            if weather_record:
                update_threshold = timezone.now() - timedelta(minutes=30)
                if weather_record.updated >= update_threshold:
                    return {
                        'temperature': weather_record.temperature,
                        'pressure': weather_record.pressure,
                        'wind_speed': weather_record.wind_speed,
                    }

            # Use the YandexWeatherAPI to get data
            yandex_weather_data = YandexWeatherAPI.get_weather_data(latitude, longitude)

            # Update or create the Weather record
            Weather.objects.update_or_create(
                latitude=latitude,
                longitude=longitude,
                city=translated_city_name,
                defaults={
                    'temperature': yandex_weather_data['temperature'],
                    'pressure': yandex_weather_data['pressure'],
                    'wind_speed': yandex_weather_data['wind_speed'],
                }
            )

            return yandex_weather_data