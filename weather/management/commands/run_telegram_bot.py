from django.core.management.base import BaseCommand
from weather.views import WeatherAPIView

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **options):
        weather_api_view = WeatherAPIView()
        weather_api_view.configure_telegram_bot()
