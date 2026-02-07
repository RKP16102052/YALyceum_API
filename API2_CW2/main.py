import sys
import requests

from geocoder import geocode
from scale import get_spn

STATIC_API = "https://static-maps.yandex.ru/1.x/"

def main():
    address = input("Введите адрес: $-> ")

    toponym = geocode(address)
    if not toponym:
        print("Объект не найден")
        return

    # координаты объекта
    lon, lat = toponym["Point"]["pos"].split()

    # подбор масштаба
    spn_x, spn_y = get_spn(toponym)

    params = {
        "ll": f"{lon},{lat}",
        "spn": f"{spn_x},{spn_y}",
        "l": "map",
        # точка по адресу объекта
        "pt": f"{lon},{lat},pm2rdm"
    }

    response = requests.get(STATIC_API, params=params)
    response.raise_for_status()

    with open("map.png", "wb") as f:
        f.write(response.content)

    print("Карта сохранена как map.png")

if __name__ == "__main__":
    main()
