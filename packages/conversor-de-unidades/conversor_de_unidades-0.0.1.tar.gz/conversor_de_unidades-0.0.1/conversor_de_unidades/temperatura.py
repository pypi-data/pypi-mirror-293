
def fahrenheit_para_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * (5 / 9)
    return celsius


def celsius_para_fahrenheit(celsius):
    fahrenheit = (celsius * (9/5)) + 32
    return fahrenheit


def celsius_para_kelvin(celsius):
    kelvin = celsius + 273.15
    return kelvin


def kelvin_para_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius
