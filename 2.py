import folium
import os


def create_path_map(path_coordinates: list, output_file: str = 'media/map.html') -> None:
    """
    Создает карту с линией маршрута и маркером в средней точке.

    :param path_coordinates: Список координат маршрута в формате [[lat, lon], ...].
    :param output_file: Путь для сохранения HTML-файла карты.
    """
    route_map = folium.Map(location=path_coordinates[0], zoom_start=11)

    for start_point, end_point in zip(path_coordinates[:-1], path_coordinates[1:]):
        folium.PolyLine([start_point, end_point], color='blue', weight=2.5).add_to(route_map)

    middle_index = len(path_coordinates) // 2
    middle_point = path_coordinates[middle_index]
    folium.Marker(location=middle_point, popup='Средняя точка пути').add_to(route_map)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    route_map.save(output_file)
    print(f"Карта сохранена в файле '{output_file}'")


if __name__ == '__main__':
    route_coordinates = [
        [55.751244, 37.618423],  # Красная площадь
        [55.715551, 37.554191],  # Лужники
        [55.791540, 37.559809],  # Динамо
    ]
    create_path_map(route_coordinates)
