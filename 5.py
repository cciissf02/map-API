import os
from typing import Optional

import requests
from dotenv import load_dotenv


def main() -> None:
    """
    Основная функция программы. Запрашивает у пользователя адрес и выводит информацию о ближайшей аптеке.
    """
    load_dotenv()
    api_key = os.getenv('YANDEX_API_TOKEN')

    if not api_key:
        print('Ошибка: API ключ не найден. Убедитесь, что YANDEX_API_TOKEN указан в .env файле.')
        return

    address = input('Введите адрес: ').strip()
    find_nearest_pharmacy(address, api_key)


def find_nearest_pharmacy(address: str, api_key: str) -> None:
    """
    Ищет ближайшую аптеку к заданному адресу, используя API Яндекса.

    :param address: Адрес, введенный пользователем.
    :param api_key: API ключ для Яндекс Геокодера и Поиска.
    """
    coordinates = get_coordinates_from_address(address, api_key)

    if not coordinates:
        print('Не удалось получить координаты для указанного адреса.')
        return

    pharmacy = search_nearest_pharmacy(coordinates, api_key)

    if pharmacy:
        print(f"Ближайшая аптека: {pharmacy['name']}, адрес: {pharmacy['address']}")
    else:
        print('Аптеки поблизости не найдены.')


def get_coordinates_from_address(address: str, api_key: str) -> Optional[tuple]:
    """
    Получает координаты (широта, долгота) для указанного адреса.

    :param address: Адрес, введенный пользователем.
    :param api_key: API ключ для Яндекс Геокодера.
    :return: Кортеж (долгота, широта) или None в случае ошибки.
    """
    geocoder_url = 'https://geocode-maps.yandex.ru/1.x/'
    params = {'apikey': api_key, 'geocode': address, 'format': 'json'}

    try:
        response = requests.get(geocoder_url, params=params)
        response.raise_for_status()
        geo_data = response.json()
        position = geo_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        lon, lat = map(float, position.split())
        return lon, lat
    except (IndexError, KeyError):
        print('Адрес не найден.')
    except requests.RequestException as error:
        print(f'Ошибка при запросе координат: {error}')
    return None


def search_nearest_pharmacy(coordinates: tuple, api_key: str) -> Optional[dict]:
    """
    Ищет ближайшую аптеку к заданным координатам.

    :param coordinates: Кортеж (долгота, широта).
    :param api_key: API ключ для Яндекс Поиска.
    :return: Словарь с информацией об аптеке или None, если аптека не найдена.
    """
    search_url = 'https://search-maps.yandex.ru/v1/'
    params = {
        'apikey': api_key,
        'text': 'аптека',
        'lang': 'ru_RU',
        'll': f'{coordinates[0]},{coordinates[1]}',
        'type': 'biz',
        'results': 1,
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        search_data = response.json()
        pharmacy_data = search_data['features'][0]['properties']
        return {
            'name': pharmacy_data['name'],
            'address': pharmacy_data['CompanyMetaData']['address'],
        }
    except (IndexError, KeyError):
        print('Аптеки поблизости не найдены.')
    except requests.RequestException as error:
        print(f'Ошибка при запросе аптеки: {error}')
    return None


if __name__ == '__main__':
    main()
