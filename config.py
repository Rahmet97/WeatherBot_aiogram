import requests

API_TOKEN = '1785801701:AAFNjZ68GzU6VO5oKMSKxpuaGds-Rjn3DD8'
API_weather = '11383a422946d6690d8e97982829c739'
api_url = 'https://api.openweathermap.org/data/2.5/weather'


def getWeather(city):
    r = requests.post(url=api_url, params={'q': city, 'APPID': API_weather, 'units': 'metric'})
    return r