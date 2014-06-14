import asyncio
import aiohttp
import json
import csv
import math
import time
import tqdm
import urllib.request

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
RADIUS = 100
SPACING = 2*RADIUS/math.sqrt(2)

LAT_STEP = SPACING*LAT_DEG_P_M
LON_STEP = SPACING*LON_DEG_P_M

LAT_CALLS = int(math.floor((LAT_MAX - LAT_MIN + LAT_STEP)/(LAT_STEP)))
LON_CALLS = int(math.floor((LON_MAX - LON_MIN + LON_STEP)/(LON_STEP)))

sem = asyncio.Semaphore(5)

def init_locations():
    location_list = []
    for i in range(LAT_CALLS):
        cur_lat = LAT_MIN + i*LAT_STEP
        for j in range(LON_CALLS):
            cur_lon = LON_MIN + j*LON_STEP
            cur_str = '{:.6f},{:.6f}' .format(cur_lat,cur_lon)
            location_list.append(cur_str)
    return location_list

@asyncio.coroutine
def get(*args, **kwargs):
    response = yield from aiohttp.request('GET', *args, **kwargs)
    return (yield from response.read_and_close(decode=True))


@asyncio.coroutine
def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        yield from f

def got_result(future):
    print("### DONE ###")
    loop.stop()

def parse_json_data(json_data, place_ref_dict):
    if json_data['status'] == 'ZERO_RESULTS':
        return ''
    elif json_data['status'] == 'OK':
        for place in json_data['results']:
            place_id = str(place['id'])
            if place_id in place_ref_dict.keys():
                print('#################################################')
                print('Places ID already processed %s' % place_id)
                return ''
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
                    place_list.append(place_id)
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
                place_ref_dict[place_id] = place_list
                return place_list

@asyncio.coroutine
def fetch_json(location):
    #Key word search, for multiple 'coffee+cafe'
    KEYWORD = 'coffee'
    TYPE = 'cafe'

    url =  ('https://maps.googleapis.com/maps/api/place/search/json?keyword=%s&location=%s'
                     '&radius=%s&sensor=false&key=%s') % (KEYWORD, location, RADIUS, AUTH_KEY)
    print('Requesting from URL %s' % url)
    place_ref_dict = {}

    with (yield from sem):
        try:
            response = yield from get(url)
        except Exception as exc:
            print('...', url, 'has error', repr(str(exc)))
            return ''
        else:        
            print(response)
            str_response = response.decode('utf-8')

            # Get the response and use the JSON library to decode the JSON
            json_data = json.loads(str_response)

            # Iterate through the results and print them to the console
            return parse_json_data(json_data, place_ref_dict)
        

def init_file():
    with open('data.csv','wt') as f1:
        writer=csv.writer(f1, delimiter=',',lineterminator='\n',)
        writer.writerow(['rating','name','reference','price_level','lat','lon','opening_hours','vicinity','photos','id','types','icon'])            
        f1.close()

def write_to_file(row):
    with open('data.csv','a') as f1:
        writer=csv.writer(f1, delimiter=',',lineterminator='\n',)
        if (row != ''):
            writer.writerow(row)
        f1.close()

def main():
    init_file()
    locations = init_locations()
    # locations = locations[:5]
    # loop = asyncio.get_event_loop()

    # single task with callback
    # task = asyncio.async(fetch_json(locations[0]))
    # task.add_done_callback(write_to_file)
    # loop.run_until_complete(task)

    # list of tasks with callback
    coros = [fetch_json(location) for location in locations]
    for completed in asyncio.as_completed(coros):
        result = yield from completed
        write_to_file(result)    

            # results.append(result)
    # f = wait_with_progress(fs)
    # asyncio.as_completed(fs)
    # task.add_done_callback(write_to_file)
    # loop.run_until_complete(f)

    # loop.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())