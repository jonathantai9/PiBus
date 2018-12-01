import xml.etree.ElementTree as ET
from urllib.request import urlopen
import time

# Grab New Brunswick Routes
url = urlopen('http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=routeList')
route_list = ET.parse(url)
routes = {}
# not in the New Brunswick campus
banned_tags = ['kearney', 'penn', 'pennexpr', 'mdntpenn', 'connect', 'rbhs', 'housing', 'ccexp']

for route in route_list.getroot().findall('route'):
    tag = route.get('tag')
    title = route.get('title')
    if tag not in banned_tags:
        routes[tag] = title

print("Routes: " + ", ".join(key + ": " + value for value, key in routes.items()))

valid_route = False
while valid_route is False:
    route = input('Enter route tag')
    if route not in routes.keys():
        print("Invalid route")
    else:
        valid_route = True

time_start = time.time()
url = urlopen('http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=routeConfig&r=' + route)
route_stops = ET.parse(url)

# Prints all stops in the route along with their bus arrival times
for stop in route_stops.getroot().findall('./route/stop'):
    stop_id = stop.get('stopId')
    url = urlopen('http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers'
                  '&command=predictions&stopId=' + stop_id + '&r=' + route)
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

time_end = time.time()

print("Time Taken: " + str(time_end - time_start))