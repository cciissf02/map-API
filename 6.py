import random
from io import BytesIO
from typing import Optional, List, Dict

import requests
from PIL import Image


def main() -> None:
    """
    Основная функция программы. Выбирает случайный город, параметры карты и отображает карту.
    """
    cities = [
        {'name': 'Москва', 'coords': [55.7558, 37.6173]},
        {'name': 'Париж', 'coords': [48.8566, 2.3522]},
        {'name': 'Нью-Йорк', 'coords': [40.7128, -74.0060]},
        {'name': 'Токио', 'coords': [35.6895, 139.6917]},
    ]

    selected_city = random.choice(cities)
    zoom_level = random.randint(13, 15)
    map_layer = random.choice(['sat', 'map'])

    print(f"Выбран город: {selected_city['name']}, масштаб: {zoom_level}, слой карты: {map_layer}")

    image_data = fetch_city_map(selected_city, zoom_level, map_layer)

    if image_data:
        display_image(image_data)
    else:
        print('Ошибка при получении изображения карты.')


def fetch_city_map(city: Dict[str, List[float]], zoom: int, map_type: str) -> Optional[bytes]:
    """
    Получает карту города с Яндекс Карт.

    :param city: Словарь с названием города и его координатами.
    :param zoom: Уровень масштабирования карты (от 1 до 17).
    :param map_type: Тип карты ('sat' для спутникового снимка, 'map' для стандартной карты).
    :return: Данные изображения карты в байтах или None в случае ошибки.
    """
    base_url = 'https://static-maps.yandex.ru/1.x/'
    params = {
        'll': f"{city['coords'][1]},{city['coords'][0]}",
        'z': zoom,
        'size': '600,400',
        'l': map_type,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.content
    except requests.RequestException as error:
        print(f"Ошибка при загрузке карты для города {city['name']}: {error}")
        return None


def display_image(image_data: bytes) -> None:
    """
    Отображает изображение, полученное в виде байтов.

    :param image_data: Данные изображения в байтах.
    """
    try:
        image = Image.open(BytesIO(image_data))
        image.show()
    except Exception as error:
        print(f"Ошибка при отображении изображения: {error}")


if __name__ == '__main__':
    main()
