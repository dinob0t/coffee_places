
import asyncio
import aiohttp
import math
import time
import urllib.request

def generate_url_list(base_url, year):
  url_list = []
  file_list = []
  year_str = str(year)
  for month in range(1,13):
    month_str = str(month)
    if month<10:
      month_str = '0'+ month_str

    for day in range(1,32):
      day_str = str(day)
      if day<10:
        day_str = '0'+ day_str

      for hour in range(0,24):
        hour_str= str(hour)
        if hour<10:
          hour_str = '0'+ hour_str        

        for minute_str in ['0000', '1500', '3000', '4500']:
          file_str = year_str + month_str + day_str + '_' + hour_str + minute_str + '_M_512.jpg'
          file_list.append(file_str)
          url_list.append(base_url + year_str + '/' + month_str + '/' + day_str + '/' +  file_str)
  return url_list, file_list

@asyncio.coroutine
def save_to_file(img, idx, file_list):
  file_name = file_list[idx]
  f = open('./2011/' + file_name,'wb')
  f.write(img)
  f.close()

@asyncio.coroutine
def fetch(url):
  data = ""
  try:
    yield from asyncio.sleep(1)
    response = yield from aiohttp.request('GET', url, connector=connector)
  except Exception as exc:
      print("ERROR ", url, 'has error', repr(str(exc)))
  else:
      data = (yield from response.read())
      print()
      response.close()

  return data

@asyncio.coroutine
def fetch_image(url, idx, file_list):
    print("fetching image with idx %d", idx)
    page = yield from fetch(url)
    print("got image with idx %d", idx)

    # save image to file
    yield from save_to_file(page, idx, file_list)

@asyncio.coroutine
def process_batch_of_urls(round, urls, file_list):
  print("Batch %d starting" % round)
  coros = []
  for idx, url in enumerate(urls):
    coros.append(asyncio.Task(fetch_image(url, idx, file_list)))

  yield from asyncio.gather(*coros)
  print("Round %d finished" % round)

@asyncio.coroutine
def process_all():
  print('### Started ###')
  start_time = time.time()
  urls, file_list = generate_url_list('http://jsoc.stanford.edu/data/hmi/images/', 2011)

  chunks=[urls[x:x+100] for x in range(0, len(urls), 100)]
  print("Total number of batches %d" % len(chunks))

  for idx, batch in enumerate(chunks):
    yield from process_batch_of_urls(idx, batch, file_list)

  total_time = time.time() - start_time
  print("Total number of api requests %d" % len(urls))
  print("Total time taken to process api requests is %s seconds" % total_time)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # connector stores cookies between requests and uses connection pool
    connector = aiohttp.TCPConnector(share_cookies=True, loop=loop)
    loop.run_until_complete(process_all())