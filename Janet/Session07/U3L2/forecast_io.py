__author__ = 'me'

import requests

#  Forecast_io retrieves json data from Forecast.io


# *========= FORECAST.IO ===========* #

def load_api_key():
    with open('forecastio_api.key', 'r') as fp:
        key = (fp.readline()).strip()
    return key

def request_data(lat_lon, timestamp):
    server = 'https://api.forecast.io/forecast'
    key = load_api_key()

    url = '%s/%s/%f,%f,%d' % (server, key, lat_lon[0], lat_lon[1],timestamp)
    r = requests.get(url)
    if r.status_code != 200:
        print ("WARNING: received a status code of ", r.status_code, " from ", url)
        return {}
    return r.json()
