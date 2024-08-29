from unittest import TestCase
from conversor_de_unidades.temperatura import (fahrenheit_para_celsius,
                                               celsius_para_fahrenheit,
                                               celsius_para_kelvin,
                                               kelvin_para_celsius)


class TestTemperatura(TestCase):
    def test_fahrenheit_para_celsius(self):
        self.assertEqual(fahrenheit_para_celsius(32), 0)
        self.assertEqual(fahrenheit_para_celsius(42), 5.555555555555555)
        self.assertEqual(fahrenheit_para_celsius(18), -7.777777777777779)

    def test_celsius_para_fahrenheit(self):
        self.assertEqual(celsius_para_fahrenheit(0), 32)
        self.assertEqual(celsius_para_fahrenheit(5.555555555555555), 42)
        self.assertEqual(celsius_para_fahrenheit(-7.777777777777779), 18)

    def test_celseius_para_kelvin(self):
        self.assertEqual(celsius_para_kelvin(0), 273.15)
        self.assertEqual(celsius_para_kelvin(4), 277.15)

    def test_kelvin_para_celsius(self):
        self.assertEqual(kelvin_para_celsius(277.15), 4)
        self.assertEqual(kelvin_para_celsius(273.15), 0)
