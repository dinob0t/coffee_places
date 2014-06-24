import asyncio
import aiohttp
import json
import csv
import math
import time
import urllib.request
import logging

# Set the Places API key for your application
AUTH_KEY = 'AIzaSyBvTCnjwofaUqzwma6gtWOyJIqTNOTStGg'

# Search bounds
# Original Manhattan and Brooklyn bounds
# LAT_MAX = 40.885457
# LAT_MIN = 40.568874

# LON_MAX = -73.854017
# LON_MIN = -74.036351

json_data = open('nyc.json')
nyc_all = json.load(json_data)
json_data.close()

LAT_MAX = 40.885457
LAT_MIN = 40.568874

LON_MAX = -73.854017
LON_MIN = -74.036351

for feature in nyc_all['features']:
  cur_poly = feature['geometry']['coordinates'][0]
  for point in cur_poly:
    if point[0] < LON_MIN:
      LON_MIN = point[0]
    if point[0] > LON_MAX:
      LON_MAX = point[0]
    if point[1] < LAT_MIN:
      LAT_MIN = point[1]
    if point[1] > LAT_MAX:
      LAT_MAX = point[1]    

print ('Bounds are:', LAT_MIN, LAT_MAX, LON_MIN, LON_MAX)

# Rough translation of degrees to meters f
LAT_DEG_P_M = (40.727740 - 40.726840)/100
LON_DEG_P_M = (-73.978720 - -73.979907 )/100

# Define the radius (in meters) for the search
RADIUS = 100
SPACING = 2*RADIUS/math.sqrt(2)

LAT_STEP = SPACING*LAT_DEG_P_M
LON_STEP = SPACING*LON_DEG_P_M

LAT_CALLS = int(math.floor((LAT_MAX - LAT_MIN + LAT_STEP)/(LAT_STEP)))
LON_CALLS = int(math.floor((LON_MAX - LON_MIN + LON_STEP)/(LON_STEP)))

place_ref_dict = {}
errors_dict ={}

# Check if points lie within a polygon
def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def init_locations():

  test_poly = [(0,0)]
  location_list = []
  for i in range(LAT_CALLS):
      cur_lat = LAT_MIN + i*LAT_STEP
      for j in range(LON_CALLS):
          cur_lon = LON_MIN + j*LON_STEP
          if point_in_poly(cur_lon,cur_lat,test_poly):
            cur_str = '{:.6f},{:.6f}' .format(cur_lat,cur_lon)
            location_list.append(cur_str)
          else:
            for feature in nyc_all['features']:
                  cur_poly = feature['geometry']['coordinates'][0]
                  test_poly = [tuple(l) for l in cur_poly]
                  if point_in_poly(cur_lon,cur_lat,test_poly):
                      cur_str = '{:.6f},{:.6f}' .format(cur_lat,cur_lon)
                      location_list.append(cur_str)
                      break        
  logging.info("total number of locations to query %d" % len(location_list))
  return location_list

def init_urls_from_locations():
  locations = init_locations()
  KEYWORD = 'coffee'
  #TYPE = 'cafe'

  urls = []
  for location in locations:
    url =  ('https://maps.googleapis.com/maps/api/place/search/json?keyword=%s&location=%s'
                     '&radius=%s&sensor=false&key=%s') % (KEYWORD, location, RADIUS, AUTH_KEY)
    urls.append(url)

  return urls

def write_to_file():
  with open('data_async.csv','wt') as f1:
    writer=csv.writer(f1, delimiter=',',lineterminator='\n',)
    writer.writerow(['rating','name','reference','price_level','lat','lon','opening_hours','vicinity','photos','id','types','icon'])
    # dump data from dict
    print("Total number of records %d" % len(place_ref_dict))
    for k,row in place_ref_dict.items():
      if (row != '' or row != 'None'):
          writer.writerow(row)

def write_errors_to_file():
  with open('errors.csv','wt') as f1:
    writer=csv.writer(f1, delimiter=',',lineterminator='\n',)
    writer.writerow(['id', 'error'])
    # dump data from dict
    print("Total number of duplicates recorded %d" % len(errors_dict))
    for k,row in errors_dict.items():
      if (row != '' or row != 'None'):
          writer.writerow(row)

@asyncio.coroutine
def parse_json_data(json_data):
  if json_data['status'] == 'OK':
    for place in json_data['results']:
      if str(place['id']) in place_ref_dict.keys():
        global errors_dict
        errors_dict[str(place['id'])] = 'ERROR'
        logging.error('#################################################')
        logging.error("Places ID already processed %s" % str(place['id']))
      else:
        place_list = []

        if 'rating' in place.keys():
            place_list.append(str(place['rating']))
        else:
            place_list.append('')

        if 'name' in place.keys():
            place_list.append((place['name']))
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
        global place_ref_dict
        place_ref_dict[str(place['id'])] = place_list
        print(place_list)

@asyncio.coroutine
def fetch(url):
  data = ""
  try:
    yield from asyncio.sleep(1)
    response = yield from aiohttp.request('GET', url, connector=connector)
  except Exception as exc:
      print("ERROR ", url, 'has error', repr(str(exc)))
  else:
      data = (yield from response.read()).decode('utf-8', 'replace')
      response.close()

  return data

@asyncio.coroutine
def print_page(url, idx):
    print("fetching page with idx %d", idx)
    page = yield from fetch(url)
    print("got page with idx %d", idx)

    # Get the response and use the JSON library to decode the JSON
    json_data = json.loads(page)
    # Iterate through the results and print them to the console
    yield from parse_json_data(json_data)

@asyncio.coroutine
def process_batch_of_urls(round, urls):
  print("Batch %d starting" % round)
  coros = []
  for idx, url in enumerate(urls):
    coros.append(asyncio.Task(print_page(url, idx)))

  yield from asyncio.gather(*coros)
  print("Round %d finished" % round)

@asyncio.coroutine
def process_all():
  logging.info('### Started ###')
  start_time = time.time()
  urls = init_urls_from_locations()

  chunks=[urls[x:x+100] for x in range(0, len(urls), 100)]
  print("Total number of batches %d" % len(chunks))

  for idx, batch in enumerate(chunks):
    yield from process_batch_of_urls(idx, batch)

  write_to_file()
  write_errors_to_file()
  total_time = time.time() - start_time
  print("Total number of api requests %d" % len(urls))
  print("Total time taken to process api requests is %s seconds" % total_time)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # connector stores cookies between requests and uses connection pool
    connector = aiohttp.TCPConnector(share_cookies=True, loop=loop)
    loop.run_until_complete(process_all())
