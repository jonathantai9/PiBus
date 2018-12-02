import xml.etree.ElementTree as ET
from urllib.request import urlopen
import time, sys
from math import radians, sin, cos, atan2, sqrt

# Next Bus Public API - http://api.rutgers.edu/
# Documentation - https://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf
base_url = 'http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command='

# Grab New Brunswick Routes
url = urlopen(base_url + 'routeList')
route_list = ET.parse(url)
routes = {}
# not in the New Brunswick campus
banned_tags = ['kearney', 'penn', 'pennexpr', 'mdntpenn', 'connect', 'rbhs', 'housing', 'ccexp']

for route in route_list.getroot().findall('route'):
    tag = route.get('tag')
    title = route.get('title')
    if tag not in banned_tags:
        routes[tag] = title

print("Routes: " + " ".join(key + "(" + value + ")" for value, key in routes.items()))

valid_route = False
while valid_route is False:
    route = input('Enter route tag')
    if route not in routes.keys():
        print("Invalid route")
    else:
        valid_route = True

def get_route_data(route):
    # Check if the route is active by checking if there are no buses active
    url = urlopen(base_url + 'vehicleLocations&r=' + route + '&t=0')
    active_buses = ET.parse(url)
    if active_buses.getroot().find('vehicle') is None:
        print('The ' + routes[route] + ' route is currently inactive.')
        quit()

    url = urlopen(base_url + 'routeConfig&r=' + route)
    route_stops = ET.parse(url)

    # Prints all stops in the route along with their bus arrival times
    for stop in route_stops.getroot().findall('./route/stop'):
        stop_id = stop.get('stopId')
        url = urlopen(base_url + 'predictions&stopId=' + stop_id + '&r=' + route)
        route_predictions = ET.parse(url)
        minutes = []

        # Check if bus stop is closed
        if route_predictions.getroot().find('./predictions/direction') is None:
            print(stop.get('title') + " is offline.")
            continue

        # Add arrival times to array
        for prediction in route_predictions.getroot().findall('.//prediction'):
            minute = prediction.get('minutes')
            if minute == '0':
                minute = '<1'
            minutes.append(minute)

        print(stop.get('title') + ':', ", ".join(minutes) + ' minutes')

def distance_between(lat1, long1, lat2, long2):
    lat1 = radians(lat1)
    long1 = radians(long1)
    lat2 = radians(lat2)
    long2 = radians(long2)

    delta_lat = lat2 - lat1
    delta_long = long2 - long1

    a = (sin(delta_lat / 2))**2 + cos(lat1) * cos(lat2) * (sin(delta_long / 2))**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6373 # radius of the Earth in km
    distance = R * c
    return distance

def get_closest_stop(route):
    current_lat = 40.50199
    current_long = -74.44826
    closest_distance = sys.maxsize
    closest_stop = ''
    url = urlopen(base_url + 'routeConfig&r=' + route)
    route_stops = ET.parse(url)

    # Loops through all stops in the given route and finds the closest one to the Honors College
    for stop in route_stops.getroot().findall('./route/stop'):
        distance = distance_between(current_lat, current_long, float(stop.get('lat')), float(stop.get('lon')))
        if distance < closest_distance:
            closest_distance = distance
            closest_stop = stop.get('title')

    return closest_stop

time_start = time.time()
get_route_data(route)
print("The closest stop in this route is: " + get_closest_stop(route))
time_end = time.time()
print("Processing Time: " + str(time_end - time_start) + 's')