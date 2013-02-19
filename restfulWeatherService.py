"""
restfulWeatherService.py
Mayank Gureja
02/17/2013
CS 480
"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from time import sleep
from urlparse import urlparse
from urllib2 import urlopen
import json
import gzip
import cStringIO
from datetime import datetime


class WebServer(BaseHTTPRequestHandler):

    def setup(self):
        """
        Constructor for WebServer class
        """
        BaseHTTPRequestHandler.setup(self)

    def do_GET(self):
        """
        Handler for the GET requests
        """

        # Parse URL
        parsed = urlparse(self.path)
        path = parsed[2]  # Path minus the host and port
        pathlist = path[1:].split('/')

        if len(pathlist) >= 3 and pathlist[0] == "MyService" and pathlist[1] == "rest" and pathlist[2].isdigit():  # If valid REST query
            zipcode = pathlist[2]

            response = weatherUnderground(zipcode)  # Get JSON response

            self.send_response(200)
            self.send_header('Content-Type', 'text/json')
            self.send_header('Content-Length', len(response))
            self.send_header('Content-Encoding', 'gzip')
            self.end_headers()

            self.wfile.write(response)

        else:  # Not a valid REST query
            weather_dict = {}
            weather_dict["error_type"] = "querynotfound"
            weather_dict["description"] = "Not a valid query to this RESTful server"
            return_json_string = json.dumps(weather_dict)  # Converting parsed data to JSON
            response = compressBuf(return_json_string)  # Compressing JSON using gzip

            self.send_response(200)
            self.send_header('Content-Type', 'text/json')
            self.send_header('Content-Length', len(response))
            self.send_header('Content-Encoding', 'gzip')
            self.end_headers()

            self.wfile.write(response)

        return


def compressBuf(buf):
    """
    Compresses given data using gzip
    """

    zbuf = cStringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', fileobj=zbuf, compresslevel=9)
    zfile.write(buf)
    zfile.close()
    return zbuf.getvalue()


def weatherUnderground(zipcode):
    """
    Queries WeatherUnderground.com for weather information
    """

    API_Key = ""
    BASE_PATH = "http://api.wunderground.com/api/" + API_Key + "/conditions/q/" + zipcode + ".json"
    weather_dict = {}
    error = False

    f = urlopen(BASE_PATH)
    json_string = f.read()
    parsed_json = json.loads(json_string)

    # Checking for errors while querying server
    for data in parsed_json['response']:
        if data == "error":
            error = True

    if error:
        weather_dict["error_type"] = parsed_json['response']['error']['type']
        weather_dict["description"] = parsed_json['response']['error']['description']
    else:
        weather_dict["city"] = parsed_json['current_observation']['display_location']['city']
        weather_dict["state"] = parsed_json['current_observation']['display_location']['state']
        weather_dict["country"] = parsed_json['current_observation']['display_location']['country']
        weather_dict["zipcode"] = parsed_json['current_observation']['display_location']['zip']
        weather_dict["area"] = parsed_json['current_observation']['observation_location']['city']
        day = parsed_json['current_observation']['local_time_rfc822'].replace(",", "").split()
        weather_dict["date"] = day[0] + " " + day[1] + " " + day[2] + " " + day[3]
        weather_dict["time"] = datetime.strptime(day[4], '%H:%M:%S').strftime('%I:%M%p').lower()
        weather_dict["weather"] = parsed_json['current_observation']['weather']
        weather_dict["temperature_string"] = parsed_json['current_observation']['temperature_string']
        weather_dict["temp_c"] = parsed_json['current_observation']['temp_c']
        weather_dict["temp_f"] = parsed_json['current_observation']['temp_f']
        weather_dict["relative_humidity"] = parsed_json['current_observation']['relative_humidity']
        weather_dict["wind_string"] = parsed_json['current_observation']['wind_string']
        weather_dict["wind_dir"] = parsed_json['current_observation']['wind_dir']
        weather_dict["wind_mph"] = parsed_json['current_observation']['wind_mph']
        weather_dict["wind_gust_mph"] = parsed_json['current_observation']['wind_gust_mph']
        weather_dict["wind_kph"] = parsed_json['current_observation']['wind_kph']
        weather_dict["wind_gust_kph"] = parsed_json['current_observation']['wind_gust_kph']
        weather_dict["feelslike_string"] = parsed_json['current_observation']['feelslike_string']
        weather_dict["feelslike_c"] = parsed_json['current_observation']['feelslike_c']
        weather_dict["feelslike_f"] = parsed_json['current_observation']['feelslike_f']
        weather_dict["icon_url"] = parsed_json['current_observation']['icon_url']

    return_json_string = json.dumps(weather_dict)  # Converting parsed data to JSON
    json_gzip = compressBuf(return_json_string)  # Compressing JSON using gzip
    f.close()

    return json_gzip


try:
    # Create a web server and define the handler to manage the incoming request
    server = HTTPServer(('localhost', 8080), WebServer)
    print "INFO: I am listening at %s" % (str(server.socket.getsockname()))
    print "* Web Server is ready to accept connections! *\n"

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print "\nINFO: KeyboardInterrupt"

    print "* Closing all sockets... *\n"
    server.server_close()

    for i in range(3, 0, -1):
        sleep(1)
        print "* Exiting in... %s second(s) *" % i

    print "\n* Goodbye! *\n"
    sleep(1)
    exit(0)
