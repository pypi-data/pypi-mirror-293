import requests
import os
import json
from datetime import datetime
from weather_ascii import ascii_arts

API_KEY = os.getenv("API_KEY_CLIMACAST")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q="
IP_INFO_URL = "https://ipinfo.io/json"

def take_manual_city_input():
    return input("Please enter the city name: ")

def get_location_from_ip():
    try:
        ip_info_response = requests.get(IP_INFO_URL)
        if ip_info_response.status_code == 200:
            ip_data = ip_info_response.json()
            return ip_data.get("city")
        else:
            print(f"IpInfo request failed with status code: {ip_info_response.status_code}")
            print("Opting for manual input of city...")
            return take_manual_city_input()
    except requests.RequestException as e:
        print(f"Error during IpInfo request to get location: {e}")
        print("Opting for manual input of city...")
        return take_manual_city_input()

def make_call_to_wm(city_name):
    url = f"{BASE_URL}{city_name}&appid={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            print(f"API request failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error during API request: {e}")
        return None

def get_sun_times(system_object):
    rise_timestamp = system_object.get("sunrise", 0)
    set_timestamp = system_object.get("sunset", 0)

    sunrise_time = datetime.fromtimestamp(rise_timestamp).strftime("%H:%M")
    sunset_time = datetime.fromtimestamp(set_timestamp).strftime("%H:%M")

    return sunrise_time, sunset_time

def parse_data(weather_response):
    try:
        root_object = json.loads(weather_response)
        weather_array = root_object.get("weather", [])
        weather_object = weather_array[0] if weather_array else {}
        main_object = root_object.get("main", {})
        system_object = root_object.get("sys", {})
        wind_object = root_object.get("wind", {})

        country = system_object.get("country", "")
        city = root_object.get("name", "")
        location = f"{city}, {country}"

        temperature = f"{main_object.get('temp', 0) - 273.15:.2f} °C"
        feels_like = f"{main_object.get('feels_like', 0) - 273.15:.2f} °C feels like"
        condition = weather_object.get("main", "")

        humidity = f"{main_object.get('humidity', 0)}%"
        wind_speed = f"{wind_object.get('speed', 0):.2f} meters per second"
        pressure = f"{main_object.get('pressure', 0)} hPa"
        visibility = f"{root_object.get('visibility', 0) / 1000.0:.2f} km"
        sunrise, sunset = get_sun_times(system_object)

        weather_condition_id = f"{weather_object.get('id', 0)}"

        return [
            " ", location, temperature, feels_like, condition, humidity, wind_speed, pressure,
            visibility, f"{sunrise} ↑ / {sunset} ↓", " ", weather_condition_id
        ]

    except Exception as e:
        print(f"Error parsing weather data: {e}")
        return None
    
def display_weather(weather_data):
    weather_ascii_arts = ascii_arts()
    weather_condition_id = int(weather_data[-1])

    if 200 <= weather_condition_id <= 232:
        for ascii_art, data in zip(weather_ascii_arts.thunderstorm, weather_data):
            print(f"{ascii_art} {data}")
    elif 300 <= weather_condition_id <= 321:
        for ascii_art, data in zip(weather_ascii_arts.drizzle, weather_data):
            print(f"{ascii_art} {data}")
    elif 500 <= weather_condition_id <= 531:
        for ascii_art, data in zip(weather_ascii_arts.rain, weather_data):
            print(f"{ascii_art} {data}")
    elif 600 <= weather_condition_id <= 622:
        for ascii_art, data in zip(weather_ascii_arts.snow, weather_data):
            print(f"{ascii_art} {data}")
    elif 700 <= weather_condition_id <= 781:
        for ascii_art, data in zip(weather_ascii_arts.mist, weather_data):
            print(f"{ascii_art} {data}")
    elif weather_condition_id == 800:
        for ascii_art, data in zip(weather_ascii_arts.clearDay, weather_data):
            print(f"{ascii_art} {data}")
    else:
        if weather_condition_id in [801, 802]:
            for ascii_art, data in zip(weather_ascii_arts.scatteredClouds, weather_data):
                print(f"{ascii_art} {data}")
        else:
            for ascii_art, data in zip(weather_ascii_arts.brokenClouds, weather_data):
                print(f"{ascii_art} {data}")
