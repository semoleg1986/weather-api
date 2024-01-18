from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from .models import Weather
import json

class WeatherAPITestCase(TestCase):

    def setUp(self):
        Weather.objects.create(
            city='moscow',
            temperature=20.0,
            pressure=1010.0,
            wind_speed=5.0,
            latitude=40.7128,
            longitude=-74.0060,
        )

    def test_get_weather_data_existing_record(self):
        response = self.client.get(reverse('weather_api'), {'city': 'moscow'})
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['temperature'], 20.0)
        self.assertEqual(data['pressure'], 1010.0)
        self.assertEqual(data['wind_speed'], 5.0)

    def test_get_weather_data_invalid_city(self):
        response = self.client.get(reverse('weather_api'), {'city': 'invalidcity'})
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('error', data)
