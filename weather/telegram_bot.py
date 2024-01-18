import telebot
from telebot import types
from decouple import config
import requests
import socket

telegram_token = config('TELEGRAM_TOKEN')
bot = telebot.TeleBot(telegram_token, parse_mode=None)

def get_django_address_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    addr, port = sock.getsockname()
    sock.close()
    return addr, port

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

def configure_telegram_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    configure_telegram_bot()