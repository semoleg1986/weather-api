from django.http import JsonResponse
from django.views import View
import requests
from geopy.geocoders import Nominatim
from translate import Translator
from .models import Weather
from decouple import config
from datetime import datetime, timedelta
from django.utils import timezone
import telebot
from telebot import types
telegram_token = config('TELEGRAM_TOKEN')
bot = telebot.TeleBot(telegram_token, parse_mode=None)

import socket

def get_django_address_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    addr, port = sock.getsockname()
    sock.close()
    return addr, port

class WeatherAPIView(View):
    def get(self, request):
        city_name = request.GET.get('city')
        latitude, longitude = self.get_coordinates(city_name.lower())
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
        translator = Translator(from_lang="ru", to_lang=target_language)
        translated_name = translator.translate(city_name)
        return translated_name.lower()

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttonA = types.KeyboardButton('Узнать погоду')
        markup.row(buttonA)
        bot.send_message(message.chat.id, 'Выберите действия:', reply_markup=markup)
        

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        reply_markup=types.ReplyKeyboardRemove()
        if message.text == 'Узнать погоду': 
            bot.reply_to(message, "Напишите название города", reply_markup=reply_markup)
        else:
            address, port = get_django_address_port()
            city_name = message.text
            api_url = f"http://{address}:8000/api/weather?city={city_name}"

            try:
                response = requests.get(api_url)
                response.raise_for_status()
                weather_data = response.json()

                if 'error' in weather_data:
                    bot.reply_to(message, f"Ошибка: {weather_data['error']}")
                else:
                    temperature = weather_data.get('temperature', 'N/A')
                    pressure = weather_data.get('pressure', 'N/A')
                    wind_speed = weather_data.get('wind_speed', 'N/A')

                    reply_message = f"Текущая погода:\nТемпература: {temperature}°C\nДавление: {pressure} мм рт. ст.\nСкорость ветра: {wind_speed} м/с"
                    bot.reply_to(message, reply_message)

            except requests.RequestException as e:
                bot.reply_to(message, f"Ошибка при запросе данных о погоде: {str(e)}")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttonA = types.KeyboardButton('Узнать погоду')
            markup.row(buttonA)
            bot.send_message(message.chat.id, 'Выберите действия:', reply_markup=markup)

    def configure_telegram_bot(self):
        bot.infinity_polling()

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

        yandex_api_url = f"https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}"
        yandex_api_key = config('YANDEX_API_KEY')
        headers = {"X-Yandex-API-Key": yandex_api_key}

        try:
            response = requests.get(yandex_api_url, headers=headers)
            response.raise_for_status()

            yandex_data = response.json()['fact']
            Weather.objects.update_or_create(
                latitude=latitude,
                longitude=longitude,
                city=translated_city_name,
                defaults={
                    'temperature': yandex_data['temp'],
                    'pressure': yandex_data['pressure_mm'],
                    'wind_speed': yandex_data['wind_speed'],
                }
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