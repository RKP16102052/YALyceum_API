import requests

GEOCODER_API = "https://geocode-maps.yandex.ru/1.x/"
API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"

def geocode(address):
    params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"
    }

    response = requests.get(GEOCODER_API, params=params)
    response.raise_for_status()

    feature = response.json()["response"]["GeoObjectCollection"]["featureMember"]
    if not feature:
        return None

    obj = feature[0]["GeoObject"]
    lon, lat = obj["Point"]["pos"].split()

    return {
        "coords": (float(lon), float(lat)),
        "address": obj["metaDataProperty"]["GeocoderMetaData"]["text"]
    }
