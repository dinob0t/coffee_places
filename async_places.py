import asyncio
import aiohttp
import json
import csv
import math
import time
import tqdm

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


# def first_magnet(page):
    # soup = bs4.BeautifulSoup(page)
    # a = soup.find('a', title='Download this torrent using magnet')
    # return a['href']


@asyncio.coroutine
def fetch_json(location):
    #Key word search, for multiple 'coffee+cafe'
    KEYWORD = 'coffee'
    TYPE = 'cafe'

    url =  ('https://maps.googleapis.com/maps/api/place/search/json?keyword=%s&location=%s'
                     '&radius=%s&sensor=false&key=%s') % (KEYWORD, location, RADIUS, AUTH_KEY)
    print('Requesting from URL %s' % url)
    with (yield from sem):
        page = yield from get(url, compress=True)
        print(page)
    print(url)


locations = init_locations()
sem = asyncio.Semaphore(5)
loop = asyncio.get_event_loop()
f = asyncio.wait([fetch_json(location) for location in locations])
loop.run_until_complete(f)
