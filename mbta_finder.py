import json
import urllib.request
from pprint import pprint


# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = "5cxA8qNOyrpjFPFmoySktzF831g3ULXl"
MBTA_API_KEY = "d9750f01282949ff939c2e59650ec367"


def get_formated_url(raw_data):
    data = urllib.parse.urlencode(raw_data)
    #data = data.encode('ascii')
    return  data


# A little bit of scaffolding if you want to use it
def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    We did similar thing in the previous assignment.
    """

    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding API URL formatting requirements.
    """
    query_string =  get_formated_url({'key': MAPQUEST_API_KEY, 'location': place_name})
    url = f'{MAPQUEST_BASE_URL}?{query_string}'
    #print(url) # uncomment to test the url in browser
    place_json = get_json(url)
    # pprint(place_json)
    latLng = place_json["results"][0]["locations"][0]['latLng']
    lat = latLng['lat']
    lon = latLng['lng']
    return lat, lon


def get_nearest_station(latitude, longitude, vehicle_type = None, radius = None):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    url_data = {'api_key': MBTA_API_KEY,
                 'filter[latitude]': latitude,
                 'filter[longitude]': longitude,
                 'sort':  'distance',
                 'page[limit]': 2,
                }
    if vehicle_type:
        pass
        #url_data['filter[vehicle_type]'] = vehicle_type #This filter is not working or not allowed
    if radius:
        url_data['filter[radius]'] = radius

    query_string = get_formated_url(url_data)
    url = f'{MBTA_BASE_URL}?{query_string}'
    # print(url) # uncomment to test the url in browser
    station_json = get_json(url)
    # pprint(station_json) # uncomment to see the json data
    sdata = station_json['data']

    # If data was found return this formate
    if len(sdata) == 0:
        return  '', 0, 0

    station_name = sdata[0]['attributes']['name'] # modify this so you get the correct station name
    # print(station_name) # uncomment to check it

    # try to find out where the wheelchair_boarding information is
    wheelchair_boarding = sdata[0]['attributes']['wheelchair_boarding']

    # Get the vehicle type. Ie Type of Transportation
    vehicle_type = sdata[0]['attributes']['vehicle_type']

    return station_name, wheelchair_boarding, vehicle_type


def find_stop_near(place_name, vehicle_type=None, radius=None):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    You don't need to modify this function
    """
    return get_nearest_station(*get_lat_long(place_name), vehicle_type, radius)


def main():
    # final test here
    place = input('Enter a place name in Boston such as "Fenway Park": ')
    lat, lon = get_lat_long(place)
    print(lat, lon)
    print(get_nearest_station(lat, lon))

    # final wrap-up
    print(find_stop_near(place))


if __name__ == '__main__':
    main()

