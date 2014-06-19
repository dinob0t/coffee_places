import asyncio
import aiohttp

@asyncio.coroutine
def fetch(url):
  response = yield from aiohttp.request('GET', url)
    # response = yield from response.read_and_close()
  try:
    blah = yield from response.read(True)
  except:
      response.close()
      raise
  finally:
      response.close()

  return blah

@asyncio.coroutine
def print_page(url):
    page = yield from fetch(url)
    # print(page)

@asyncio.coroutine
def process_batch_of_urls(round, urls):
  print("Round starting: %d" % round)
  coros = []
  for url in urls:
      coros.append(asyncio.Task(print_page(url)))
  yield from asyncio.gather(*coros)
  print("Round finished: %d" % round)

@asyncio.coroutine
def process_all():
  # api_url = 'https://maps.googleapis.com/maps/api/place/search/json?keyword=coffee&location=40.642696,-73.930595&radius=100&sensor=false&key=AIzaSyBvTCnjwofaUqzwma6gtWOyJIqTNOTStGg'
  # api_url = 'https://yahoo.com'
  api_url = 'https://microsoft.com'
  for i in range(10):
    urls = []
    for url in range(50):
      urls.append(api_url)
    yield from process_batch_of_urls(i, urls)


loop = asyncio.get_event_loop()
loop.run_until_complete(process_all())
