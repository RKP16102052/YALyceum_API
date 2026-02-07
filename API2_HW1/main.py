import sys
import requests

from geocoder import geocode
from organizations import get_pharmacies
from scale import get_spn_for_points

STATIC_API = "https://static-maps.yandex.ru/1.x/"


def pharmacy_style(hours):
    if hours is None:
        return "pm2grm"   # серый
    if "круглосуточ" in hours.lower():
        return "pm2gnm"   # зелёный
    return "pm2blm"       # синий


def main():
    address = input("Введите адрес: $-> ")

    point = geocode(address)
    if not point:
        print("Адрес не найден")
        return

    pharmacies = get_pharmacies(point["coords"], 100)

    points = [point["coords"]] + [p["coords"] for p in pharmacies]
    spn_x, spn_y = get_spn_for_points(points)

    pts = [f"{point['coords'][0]},{point['coords'][1]},pm2rdm"]

    for p in pharmacies:
        style = pharmacy_style(p["hours"])
        pts.append(f"{p['coords'][0]},{p['coords'][1]},{style}")

    params = {
        "ll": f"{point['coords'][0]},{point['coords'][1]}",
        "spn": f"{spn_x},{spn_y}",
        "l": "map",
        "pt": "~".join(pts)
    }

    response = requests.get(STATIC_API, params=params)
    response.raise_for_status()

    with open("map.png", "wb") as f:
        f.write(response.content)

    print("Найдено 10 аптек рядом с адресом:")
    for p in pharmacies:
        print(f"- {p['name']} ({int(p['distance'])} м)")

    print("\nКарта сохранена как map.png")


if __name__ == "__main__":
    main()
