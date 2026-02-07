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


def get_pharmacies(coords, count=10):
    spn = 0.000000000000000000002
    max_spn = 0.00005   # 🚨 ограничение (≈ 5 км)

    pharmacies = []

    while spn <= max_spn:
        params = {
            "apikey": API_KEY,
            "geocode": "аптека",
            "ll": f"{coords[0]},{coords[1]}",
            "spn": f"{spn},{spn}",
            "results": 20,
            "format": "json"
        }

        response = requests.get(GEOCODER_API, params=params)
        response.raise_for_status()

        features = response.json()["response"]["GeoObjectCollection"]["featureMember"]

        pharmacies = []
        for f in features:
            obj = f["GeoObject"]
            lon, lat = map(float, obj["Point"]["pos"].split())
            meta = obj["metaDataProperty"]["GeocoderMetaData"]

            pharmacies.append({
                "coords": (lon, lat),
                "name": meta.get("name", "Аптека"),
                "hours": meta.get("Hours", {}).get("text"),
                "distance": distance(coords, (lon, lat))
            })

        if len(pharmacies) >= count:
            break

        spn *= 2

    # сортируем по расстоянию и берём сколько нашли (до 10)
    pharmacies.sort(key=lambda x: x["distance"])
    return pharmacies[:count]
