import requests
import math

GEOCODER_API = "https://geocode-maps.yandex.ru/1.x/"
API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"


def distance(p1, p2):
    lon1, lat1 = p1
    lon2, lat2 = p2

    r = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def find_pharmacy(coords):
    spn = 0.001  # начинаем с очень маленькой области

    for _ in range(6):  # максимум ~0.064
        params = {
            "apikey": API_KEY,
            "geocode": "аптека",
            "ll": f"{coords[0]},{coords[1]}",
            "spn": f"{spn},{spn}",
            "results": 5,
            "format": "json"
        }

        response = requests.get(GEOCODER_API, params=params)
        response.raise_for_status()

        features = response.json()["response"]["GeoObjectCollection"]["featureMember"]

        if features:
            # выбираем реально ближайшую
            nearest = None
            min_dist = float("inf")

            for f in features:
                lon, lat = map(float, f["GeoObject"]["Point"]["pos"].split())
                d = distance(coords, (lon, lat))
                if d < min_dist:
                    min_dist = d
                    nearest = f["GeoObject"]

            meta = nearest["metaDataProperty"]["GeocoderMetaData"]
            lon, lat = map(float, nearest["Point"]["pos"].split())

            return {
                "coords": (lon, lat),
                "name": meta.get("name", "Аптека"),
                "address": meta["text"],
                "hours": meta.get("Hours", {}).get("text", "нет данных"),
                "distance": min_dist
            }

        spn *= 2  # расширяем область

    return None
