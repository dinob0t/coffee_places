# Import the relevant libraries
import urllib2
import json
import csv
import math
import time
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.web.client import getPage

# Set the Places API key for your application
AUTH_KEY = 'AIzaSyBvTCnjwofaUqzwma6gtWOyJIqTNOTStGg'

# Search bounds
LAT_MAX = 40.885457
LAT_MIN = 40.568874

LON_MAX = -73.854017
LON_MIN = -74.036351

LAT_DEG_P_M = (40.727740 - 40.726840)/100
LON_DEG_P_M = (-73.978720 - -73.979907 )/100

# Define the radius (in meters) for the search
RADIUS = 10000
SPACING = 2*RADIUS/math.sqrt(2)

LAT_STEP = SPACING*LAT_DEG_P_M
LON_STEP = SPACING*LON_DEG_P_M

LAT_CALLS = int(math.floor((LAT_MAX - LAT_MIN + LAT_STEP)/(LAT_STEP)))
LON_CALLS = int(math.floor((LON_MAX - LON_MIN + LON_STEP)/(LON_STEP)))

print 'Total LAT calls: ', (LAT_CALLS)
print 'Total LON calls: ', (LON_CALLS)
print 'Total calls: ', (LAT_CALLS*LON_CALLS)

location_list = []
for i in range(LAT_CALLS):
	cur_lat = LAT_MIN + i*LAT_STEP
	for j in range(LON_CALLS):
		cur_lon = LON_MIN + j*LON_STEP
		cur_str = '{:.6f},{:.6f}' .format(cur_lat,cur_lon)
		location_list.append(cur_str)

locations_length = len(location_list)
print 'total number of locations to seach for %s' % locations_length

@inlineCallbacks
def try_parallel(location):
	start_time = time.time()

	#Key word search, for multiple 'coffee+cafe'
	KEYWORD = 'coffee'
	TYPE = 'cafe'

	url =  ('https://maps.googleapis.com/maps/api/place/search/json?keyword=%s&location=%s'
			         '&radius=%s&sensor=false&key=%s') % (KEYWORD, location, RADIUS, AUTH_KEY)
	print 'Requesting from URL %s' % url
	response = yield getPage(url)
	# print response

	place_ref_dict = {}

	# Get the response and use the JSON library to decode the JSON
	json_data = json.loads(response)

	# Iterate through the results and print them to the console
	if json_data['status'] == 'OK':
		for place in json_data['results']:
			if str(place['id']) in place_ref_dict.keys():
				print 'Places ID already processed %s' % str(place['id'])
				break
			else:
				place_list = []

				if 'rating' in place.keys():
					place_list.append(str(place['rating']))
				else:
					place_list.append('')

				if 'name' in place.keys():
					place_list.append((place['name']).encode('utf8'))
				else:
					place_list.append('')

				if 'reference' in place.keys():
					place_list.append(str(place['reference']))
				else:
					place_list.append('')

				if 'price_level' in place.keys():
					place_list.append(str(place['price_level']))
				else:
					place_list.append('')

				if 'geometry' in place.keys():
					if 'location' in place['geometry'].keys():
						place_list.append(str(place['geometry']['location']['lat']))
						place_list.append(str(place['geometry']['location']['lng']))
					else:
						place_list.append('')
						place_list.append('')
				else:
					place_list.append('')
					place_list.append('')

				if 'opening_hours' in place.keys():
					place_list.append(str(place['opening_hours']))
				else:
					place_list.append('')

				if 'vicinity' in place.keys():
					place_list.append(str(place['vicinity']))
				else:
					place_list.append('')

				if 'photos' in place.keys():
					place_list.append(str(place['photos']))
				else:
					place_list.append('')

				if 'id' in place.keys():
					place_list.append(str(place['id']))
				else:
					place_list.append('')

				if 'types' in place.keys():
					place_list.append(str(place['types']))
				else:
					place_list.append('')

				if 'icon' in place.keys():
					place_list.append(str(place['icon']))
				else:
					place_list.append('')

				# update our dict
				place_ref_dict[str(place['id'])] = place_list

	# if it is the last url to process, dump in memory to file
	if (len(place_ref_dict) == 20):
		with open('data.csv','wb') as f1:
			writer=csv.writer(f1, delimiter=',',lineterminator='\n',)
			writer.writerow(['rating','name','reference','price_level','lat','lon','opening_hours','vicinity','photos','id','types','icon'])
			# loop through dict
			for k, v in place_ref_dict.items():
				writer.writerow(v)


# loop through each url and process
location_list = location_list[:6]
for l in location_list:
		try_parallel(l)

reactor.run()
