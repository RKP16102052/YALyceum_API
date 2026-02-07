import sys
import requests

from geocoder import geocode
from organizations import find_pharmacy
from scale import get_spn_for_two_points

STATIC_API = "https://static-maps.yandex.ru/1.x/"

def main():
    address = input("Введите адрес: $-> ")

    point = geocode(address)
    if not point:
        print("Адрес не найден")
        return

    pharmacy = find_pharmacy(point["coords"])

    spn_x, spn_y = get_spn_for_two_points(
        point["coords"],
        pharmacy["coords"]
    )

    params = {
        "ll": f"{point['coords'][0]},{point['coords'][1]}",
        "spn": f"{spn_x},{spn_y}",
        "l": "map",
        "pt": (
            f"{point['coords'][0]},{point['coords'][1]},pm2blm~"
            f"{pharmacy['coords'][0]},{pharmacy['coords'][1]},pm2rdm"
        )
    }

    response = requests.get(STATIC_API, params=params)
    response.raise_for_status()

    with open("map.png", "wb") as f:
        f.write(response.content)

    # ---- СНИППЕТ ----
    print("📍 Исходный адрес:")
    print(point["address"])
    print("\n💊 Ближайшая аптека:")
    print(pharmacy["name"])
    print(pharmacy["address"])
    print("Время работы:", pharmacy["hours"])
    print(f"Расстояние: {int(pharmacy['distance'])} м")

    print("\nКарта сохранена как map.png")


if __name__ == "__main__":
    main()
