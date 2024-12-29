import requests
import os


def generate_map_markers(stadiums_coordinates: dict) -> str:
    """
    Генерирует строку меток для отображения на карте.
    """
    return '~'.join([f'{coordinates},pm2rdm' for coordinates in stadiums_coordinates.values()])


def save_map_as_html(map_url: str, file_path: str) -> None:
    """
    Сохраняет карту в формате HTML.

    :param map_url: URL для получения карты.
    :param file_path: Путь для сохранения HTML-файла.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    html_content = f'<html><body><img src="{map_url}" alt="карта"></body></html>'
    with open(file_path, 'w') as file:
        file.write(html_content)
    print(f"Карта сохранена в файле '{file_path}'")


def generate_stadiums_map(
        stadiums_coordinates: dict,
        output_file: str = 'media/stadiums_map.html',
        map_size: str = '600,400'
) -> None:
    """
    Генерирует HTML-файл с картой, на которой отображены заданные стадионы.

    :param stadiums_coordinates: Словарь с названиями стадионов и их координатами.
    :param output_file: Путь для сохранения HTML-файла с картой.
    :param map_size: Размер карты в формате 'ширина,высота'.
    """
    markers = generate_map_markers(stadiums_coordinates)
    map_service_url = 'https://static-maps.yandex.ru/1.x/'
    request_params = {'l': 'map', 'size': map_size, 'pt': markers}

    try:
        response = requests.get(map_service_url, params=request_params)
        response.raise_for_status()  # Проверяет статус ответа
        save_map_as_html(response.url, output_file)
    except requests.RequestException as error:
        print(f'Ошибка при загрузке карты: {error}')


if __name__ == '__main__':
    stadiums_coordinates = {
        'Лужники': '37.554191,55.715551',
        'Спартак': '37.440262,55.818015',
        'Динамо': '37.559809,55.791540',
    }
    generate_stadiums_map(stadiums_coordinates)
