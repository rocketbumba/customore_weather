import asyncio
import aiohttp
import json

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

dic = {(10.76, 106.66): {'temperature': 299.27, 'humidity': 83, 'wind_speed': 1.54, 'name': 'Ho Chi Minh City'},
       (10.96, 106.66): {'temperature': 298.16, 'humidity': 94, 'wind_speed': 1.54, 'name': 'Thu Dau Mot'},
       (11.16, 106.66): {'temperature': 297.94, 'humidity': 92, 'wind_speed': 0.98, 'name': 'Tinh Binh Duong'}}


async def fetch_weather(session, lat: float, lon: float):
    api_key = "56ca0f5c61e4141a46f218433e9b1459"
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
    point_need_call_api = get_cities_in_bounding_box(lat_min=10.7626, lon_min=106.6602, lat_max=11.8231,
                                                     lon_max=106.7108)

    async with aiohttp.ClientSession() as session:
        tasks = []
        results = {}
        for lat, lon in point_need_call_api:
            if (lat, lon) not in dic:
                tasks.append(asyncio.create_task(fetch_weather(session, lat=lat, lon=lon)))
                results = await asyncio.gather(*tasks)
        if results is not None:
            for temp in results:
                dic.update(temp)
            print(dic)


def is_location_city(geolocator: Nominatim, point: tuple) -> bool:
    lat = point[0]
    lon = point[1]
    location = geolocator.reverse(f"{lat}, {lon}", language='en-US')
    if location:
        address = location.raw['address']
        if 'city' in address:
            return True
    return False


def get_cities_in_bounding_box(lat_min, lon_min, lat_max, lon_max) -> list:
    geolocator = Nominatim(user_agent="my_app", scheme='http', timeout=10000)
    lat_min, lon_min = 10.7626, 106.6602
    lat_max, lon_max = 11.8231, 106.7108
    point_need_to_call_api = []
    point_searched = set()
    for lat in range(int(lat_min * 100), int(lat_max * 100), 20):
        for lon in range(int(lon_min * 100), int(lon_max * 100), 20):
            point = (lat / 100, lon / 100)
            if point not in point_searched and is_location_city(geolocator, point):
                point_need_to_call_api.append(point)
                point_searched.add(point)

    return point_need_to_call_api


if __name__ == "__main__":
    asyncio.run(main())
