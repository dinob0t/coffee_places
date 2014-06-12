# Import the relevant libraries
import urllib2
import json

# Set the Places API key for your application
AUTH_KEY = 'AIzaSyB9F9VhZDwPctQnoPJdwH0xlIOVgtMdtIs'

# Define the location coordinates
LOCATION = '40.720815,-74.000675'

# Define the radius (in meters) for the search
RADIUS = 800

#Key word search, for multiple 'coffee+cafe'
KEYWORD = 'coffee'

TYPE = 'cafe'


# Compose a URL to query a predefined location with a radius of 5000 meters
# Simple place search
# url = ('https://maps.googleapis.com/maps/api/place/search/json?location=%s'
#          '&radius=%s&sensor=false&key=%s') % (LOCATION, RADIUS, AUTH_KEY)

# With search term
url =  ('https://maps.googleapis.com/maps/api/place/search/json?keyword=%s&location=%s'
         '&radius=%s&sensor=false&key=%s') % (KEYWORD, LOCATION, RADIUS, AUTH_KEY)
print url
# Search on type
# url =  ('https://maps.googleapis.com/maps/api/place/search/json?type=%slocation=%s'
#          '&radius=%s&sensor=false&key=%s') % (TYPE, LOCATION, RADIUS, AUTH_KEY)

# Send the GET request to the Place details service (using url from above)
response = urllib2.urlopen(url)

# Get the response and use the JSON library to decode the JSON
json_raw = response.read()
json_data = json.loads(json_raw)


# Iterate through the results and print them to the console
if json_data['status'] == 'OK':
	for place in json_data['results']:
		if 'rating' in place.keys():
			print str(place['name']) + ' ' + str(place['rating'])
		else:
			print str(place['name']) + ' ?'
		#print place
		#print " "
		#print '%s: %s\n' % (place['name'], place['reference'])

