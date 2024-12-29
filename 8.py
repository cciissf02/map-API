import math
import os
from typing import Optional, Tuple

import requests
from dotenv import load_dotenv


def main() -> None:
    """
    Основная функция для расчёта расстояния между домом и университетом.
    """
    load_dotenv()
    api_key = os.getenv('YANDEX_API_TOKEN')
    if not api_key:
        print('Ошибка: API ключ не найден. Проверьте файл .env.')
        return

    home_address = input('Введите адрес вашего дома: ')
    university_address = input('Введите адрес университета: ')

    home_coords = get_coordinates(home_address, api_key)
    university_coords = get_coordinates(university_address, api_key)

    if home_coords and university_coords:
        distance = calculate_distance(home_coords, university_coords)
        print(f'Расстояние от дома до университета: {distance:.2f} метров')
    else:
        print('Не удалось вычислить расстояние. Проверьте адреса и повторите попытку.')


def calculate_distance(point_a: Tuple[float, float], point_b: Tuple[float, float]) -> float:
    """
    Рассчитывает расстояние между двумя точками по их координатам.

    :param point_a: Координаты первой точки (долгота, широта).
    :param point_b: Координаты второй точки (долгота, широта).
    :return: Расстояние в метрах.
    """
    degree_to_meters_factor = 111_000
    lon_a, lat_a = point_a
    lon_b, lat_b = point_b

    avg_lat = math.radians((lat_a + lat_b) / 2.0)
    lat_lon_factor = math.cos(avg_lat)

    dx = abs(lon_a - lon_b) * degree_to_meters_factor * lat_lon_factor
    dy = abs(lat_a - lat_b) * degree_to_meters_factor

    return math.sqrt(dx ** 2 + dy ** 2)


def get_coordinates(address: str, api_key: str) -> Optional[Tuple[float, float]]:
    """
    Получает координаты (долгота, широта) для указанного адреса.

    :param address: Адрес для поиска.
    :param api_key: API ключ Яндекс Геокодера.
    :return: Кортеж с координатами (долгота, широта) или None, если запрос не удался.
    """
    geocoder_url = 'https://geocode-maps.yandex.ru/1.x/'
    params = {'apikey': api_key, 'geocode': address, 'format': 'json'}

    try:
        response = requests.get(geocoder_url, params=params)
        response.raise_for_status()
        geo_data = response.json()

        coords = geo_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        lon, lat = map(float, coords.split())
        return lon, lat
    except requests.RequestException as e:
        print(f'Ошибка при запросе геокодера для адреса "{address}": {e}')
    except (IndexError, KeyError):
        print(f'Не удалось найти координаты для адреса: "{address}". Проверьте правильность ввода.')

    return None


if __name__ == '__main__':
    main()
