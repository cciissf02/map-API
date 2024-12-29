import os
from typing import Optional, List
import requests
from dotenv import load_dotenv


def main() -> None:
    """
    Основная функция программы. Получает список городов от пользователя и определяет самый южный из них.
    """
    load_dotenv()
    api_key = os.getenv('YANDEX_API_TOKEN')
    if not api_key:
        print('Ошибка: API ключ не найден.')
        return

    city_names = input('Введите список городов через запятую: ').split(',')
    southernmost_city = find_southernmost_city(city_names, api_key)

    if southernmost_city:
        print(f'Самый южный город: {southernmost_city}')
    else:
        print('Не удалось определить самый южный город.')


def find_southernmost_city(city_names: List[str], api_key: str) -> Optional[str]:
    """
    Определяет самый южный город из списка на основе широты.

    :param city_names: Список названий городов.
    :param api_key: API ключ для Yandex Geocoder.
    :return: Название самого южного города или None, если города не удалось обработать.
    """
    base_url = 'https://geocode-maps.yandex.ru/1.x/'
    city_latitudes = {}

    for city in city_names:
        city = city.strip()
        try:
            response = requests.get(
                base_url,
                params={'apikey': api_key, 'geocode': city, 'format': 'json'}
            )
            response.raise_for_status()
            geo_data = response.json()

            position = (
                geo_data['response']
                ['GeoObjectCollection']
                ['featureMember'][0]
                ['GeoObject']['Point']['pos']
            )
            _, latitude = map(float, position.split())
            city_latitudes[city] = latitude
        except (IndexError, KeyError):
            print(f'Не удалось найти координаты для города: {city}')
        except requests.RequestException as error:
            print(f'Ошибка при запросе данных для города {city}: {error}')

    if city_latitudes:
        return min(city_latitudes, key=city_latitudes.get)
    else:
        print('Не удалось обработать ни один из городов.')
        return None


if __name__ == '__main__':
    main()
