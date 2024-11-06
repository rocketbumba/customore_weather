import asyncio
import time

import aiohttp
import json
import schedule
from geopy.geocoders import Nominatim


def read_api_key(filename="store_key.txt"):
  try:
    with open(filename, "r") as f:
      api_key = f.read().strip()
      return api_key
  except FileNotFoundError:
    print(f"File '{filename}' not found.")
    return None
  except Exception as e:
    print(f"Error reading API key from '{filename}': {str(e)}")
    return None

def save_dict_to_txt(dictionary, filename):
    converted_data = {str(key): value for key, value in dictionary.items()}
    with open(filename, 'w') as f:
        json.dump(converted_data, f, indent=2)


def read_dict_from_txt(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    weather_data = {}
    for key, value in data.items():
        latitude, longitude = map(float, key.strip('()').split(','))
        weather_data[(latitude, longitude)] = value
    return weather_data

def is_location_city(geolocator: Nominatim, point: tuple) -> bool:
    lat = point[0]
    lon = point[1]
    location = geolocator.reverse(f"{lat}, {lon}", language='en-US')
    if location:
        address = location.raw['address']
        if 'city' in address:
            return True
    return False

async def fetch_weather(session, lat: float, lon: float) -> dict:
    api_key = read_api_key()
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

    async with session.get(url) as response:
        response.raise_for_status()
        response_data = await response.json()
    return {
        (lat, lon): {
            'temperature': response_data['main']['temp'],
            'humidity': response_data['main']['humidity'],
            'wind_speed': response_data['wind']['speed'],
            'name': response_data['name'],
        },
    }


async def main():
    cache_data = read_dict_from_txt('hiep.json')
    point_need_call_api, point_already_have = get_cities_in_bounding_box(
        lat_min=10.7626,
        lon_min=106.6602,
        lat_max=11.8231,
        lon_max=106.7108,
        cache_data=cache_data,
    )

    async with aiohttp.ClientSession() as session:
        tasks = []
        response = {}
        result = {}
        for lat, lon in point_need_call_api:
            tasks.append(asyncio.create_task(fetch_weather(session, lat=lat, lon=lon)))
            response = await asyncio.gather(*tasks)

        if response is not None:
            for data_weather in response:
                cache_data.update(data_weather)
                result.update(data_weather)

        for point in point_already_have:
            key = (point[0], point[1])
            result[key] = cache_data[key]

    save_dict_to_txt(result, 'hiep.json')

    for city in result.values():
        print('City:' + city['name'])
        print('Temperature: ' + str(city['temperature']))
        print('Humidity:' + str(city['humidity']))
        print('Wind Speed: ' + str(city['wind_speed']))
        print("========")





def get_cities_in_bounding_box(lat_min, lon_min, lat_max, lon_max, cache_data: dict) -> tuple:
    geolocator = Nominatim(user_agent="my_app", scheme='http', timeout=10000)
    point_need_to_call_api = []
    point_already_have = set()
    for lat in range(int(lat_min * 100), int(lat_max * 100), 20):
        for lon in range(int(lon_min * 100), int(lon_max * 100), 20):
            point = (lat / 100, lon / 100)
            if point not in cache_data and is_location_city(geolocator, point):
                point_need_to_call_api.append(point)
            if point in cache_data :
                point_already_have.add(point)
    return point_need_to_call_api, list(point_already_have)


if __name__ == "__main__":
    asyncio.run(main())
