import sys
from climacast.weather import get_location_from_ip, make_call_to_wm, parse_data, display_weather

def main():
    city_name = None
    weather_data = None

    if len(sys.argv) > 1:
        city_name = sys.argv[1]
    else:
        city_name = get_location_from_ip()

    weather_response = make_call_to_wm(city_name)

    if weather_response is not None:
        weather_data = parse_data(weather_response.text)
    else:
        print("Failed to retrieve weather data.")

    if weather_data is not None:
        display_weather(weather_data)

if __name__ == "__main__":
    main()
