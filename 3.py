import requests
import os


def get_coordinates_from_user() -> tuple:
    """
    Запрашивает у пользователя координаты объекта.
    """
    try:
        latitude = float(input('Введите широту объекта: '))
        longitude = float(input('Введите долготу объекта: '))
        return latitude, longitude
    except ValueError:
        raise ValueError('Ошибка ввода. Введите координаты в виде десятичных чисел.')


def save_satellite_image(
        coordinates: tuple,
        zoom_level: int = 16,
        output_file: str = 'media/satellite_image.png'
) -> None:
    """
    Сохраняет спутниковый снимок объекта по заданным координатам.

    :param coordinates: Кортеж (широта, долгота) объекта.
    :param zoom_level: Уровень масштабирования карты (по умолчанию 16).
    :param output_file: Путь к файлу, в который будет сохранён снимок.
    """
    base_url = 'https://static-maps.yandex.ru/1.x/'
    params = {
        'll': f'{coordinates[1]},{coordinates[0]}',
        'z': zoom_level,
        'l': 'sat',
        'size': '600,400'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f'Ошибка при запросе снимка: {error}')
        return

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'wb') as file:
        file.write(response.content)
    print(f'Снимок успешно сохранён в файл {output_file}')


def main() -> None:
    """
    Основная функция программы. Запрашивает координаты объекта и сохраняет спутниковый снимок.
    """
    try:
        coordinates = get_coordinates_from_user()
        save_satellite_image(coordinates)
    except ValueError as error:
        print(error)


if __name__ == '__main__':
    main()
