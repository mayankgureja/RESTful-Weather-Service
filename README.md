RESTful-Weather-Service
=======================

A RESTful Web Server that returns JSON weather information to user queries

How To Run
----------

Just launch restfulWeatherService.py. There are no parameters.


Compatibility
-------------

Tested to work on Google Chrome, Firefox, Internet Explorer, Google Chrome for Android and Android Web Browser


Description
-----------

restfulWeatherService.py is a Web Server written in Python. It uses the BaseHTTPServer library to create sockets and run an always-on web service. The advantage of having used BaseHTTPServer is less coding (fewer lines) and greater flexibility and ease in coding more advanced functions.

When a client types in http://localhost:8080/MyService/rest/zipcode (zipcode = "19104", "10019" etc.), the server queries Weather Underground for weather information for that zipcode. Weather Underground allows any developer make GET requests to their servers and get weather information by zipcode, city, etc. There is no authentication protocol, so the whole thing can be done with just a browser request if you want to test this. Type this on your browser and you should get back JSON weather information for Central Park in New York City, NY:
http://api.wunderground.com/api/API-KEY/conditions/q/10019.json (NOTE: You must have an API Key for this to work. My API Key has been removed from this project for obvious security reasons. You can get your own developer API key from Weather Underground for free)

After querying Weather Underground, the server parses the JSON information and takes out the useful bits that it will send to its client, such as temperature, wind speed and other parameters. It then compresses this using gzip and sends back a response to the client with a 'Content-Encoding: gzip' tag, so the browser/client knows to expect a compressed data stream and will uncompress it before displaying/using it.

The server does not crash for any reason. It simply displays the error message and continues. In case the client requests information for an invalid zipcode, Weather Underground will send back a JSON response with an error message. This scenario is also dealt with by the web server and an appropriate response is sent back to its client.

Screenshots
-----------

Screenshots of the application in action are available in the /screenshots folder.

Dependencies/Requirements
-------------------------

Everything is part of the standard Python libraries.
