# Import the relevant libraries
import urllib2
import json
import csv
import math
import time

# Set the Places API key for your application
AUTH_KEY = 'AIzaSyB9F9VhZDwPctQnoPJdwH0xlIOVgtMdtIs'

# Search bounds
LAT_MAX = 40.885457
LAT_MIN = 40.568874

LON_MAX = -73.854017 
LON_MIN = -74.036351

LAT_DEG_P_M = (40.727740 - 40.726840)/100
LON_DEG_P_M = (-73.978720 - -73.979907 )/100

# Define the radius (in meters) for the search
RADIUS = 100
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


CALL_COUNT_MAX = 50000



#Key word search, for multiple 'coffee+cafe'
KEYWORD = 'coffee'

TYPE = 'cafe'

place_ref_dict = {}
call_count = 0
total_time = 0

with open('data.csv','wb') as f1:
	writer=csv.writer(f1, delimiter=',',lineterminator='\n',)
	writer.writerow(['rating','name','reference','price_level','lat','lon','opening_hours','vicinity','photos','id','types','icon'])

	for LOCATION in location_list:
		print 'Current location: ', LOCATION
		start_time = time.time()

		# Define the location coordinates
		#LOCATION = '40.720815,-74.000675'
		# Compose a URL to query a predefined location with a radius of 5000 meters
		# Simple place search
		# url = ('https://maps.googleapis.com/maps/api/place/search/json?location=%s'
		#          '&radius=%s&sensor=false&key=%s') % (LOCATION, RADIUS, AUTH_KEY)

		# With search term
		url =  ('https://maps.googleapis.com/maps/api/place/search/json?keyword=%s&location=%s'
		         '&radius=%s&sensor=false&key=%s') % (KEYWORD, LOCATION, RADIUS, AUTH_KEY)
		#print url
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
				if str(place['id']) not in place_ref_dict.keys():
					place_ref_dict[str(place['id'])] = ''
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

					writer.writerow(place_list)
		cur_time = time.time() - start_time
		total_time += cur_time
		call_count += 1
		average_time = total_time/call_count

		print 'Call number: ', call_count
		print 'Time remaining (s): ', average_time*(LAT_CALLS*LON_CALLS - call_count)
		if call_count > CALL_COUNT_MAX:
			print 'Call count too high: ', call_count
			break



