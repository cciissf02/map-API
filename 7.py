import os
from typing import Optional

import requests
from dotenv import load_dotenv


def main() -> None:
    """
    Основная функция для ввода адреса и определения района.
    """
    load_dotenv()
    api_key = os.getenv('YANDEX_API_TOKEN')
    if not api_key:
        print('Ошибка: API ключ не найден. Проверьте файл .env.')
        return

    address = input('Введите адрес: ')
    district = get_district_from_address(address, api_key)

    if district:
        print(f'Район: {district}')
    else:
        print('Район не найден.')


def get_district_from_address(address: str, api_key: str) -> Optional[str]:
    """
    Получает район для указанного адреса с использованием Яндекс Геокодера.

    :param address: Адрес для поиска.
    :param api_key: API ключ Яндекс Геокодера.
    :return: Название района или None, если район не найден.
    """
    geocoder_url = 'https://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {
        'apikey': api_key,
        'geocode': address,
        'format': 'json',
        'kind': 'district',
    }

    try:
        response = requests.get(geocoder_url, params=geocoder_params)
        response.raise_for_status()
        geo_data = response.json()
        district = (
            geo_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']
            ['GeocoderMetaData']['text']
        )
        return district
    except requests.RequestException as error:
        print(f'Ошибка при запросе к геокодеру: {error}')
    except (IndexError, KeyError):
        print('Ошибка обработки данных ответа: не удалось найти информацию о районе.')

    return None


if __name__ == '__main__':
    main()
