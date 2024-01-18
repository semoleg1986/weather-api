from django.core.management.base import BaseCommand
from weather.telegram_bot import configure_telegram_bot

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **options):
        configure_telegram_bot()
