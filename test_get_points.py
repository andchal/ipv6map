from unittest import TestCase
from app import get_points


class TestGet_points(TestCase):
    def test_get_points(self):
        url = 'http://localhost:5000/ipv6/api/v1.0/locations?lowerx=-60&lowery=-60&upperx=20&uppery=20'
