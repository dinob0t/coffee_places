import asyncio
import aiohttp

@asyncio.coroutine
def fetch(url):
  data = ""
  try:
    yield from asyncio.sleep(1)
    response = yield from aiohttp.request('GET', url, connector=connector)
  except Exception as exc:
      print('...', url, 'has error', repr(str(exc)))
  else:
      data = (yield from response.read()).decode('utf-8', 'replace')
      response.close()

  return data
    # response = yield from response.read_and_close()
  # try:
  #   content = yield from response.read(True)
  # except:
  #     response.close()
  #     raise
  # finally:
  #     response.close()
  #
  # return content

@asyncio.coroutine
def print_page(url, idx):
    print("fetching page with idx %d", idx)
    page = yield from fetch(url)
    print("got page with idx %d", idx)

@asyncio.coroutine
def process_batch_of_urls(round, urls):
  print("Round starting: %d" % round)
  coros = []
  for idx, url in enumerate(urls):
    coros.append(asyncio.Task(print_page(url, idx)))

  # for url in urls:
  #     coros.append(asyncio.Task(print_page(url)))
  yield from asyncio.gather(*coros)
  print("Round finished: %d" % round)

@asyncio.coroutine
def process_all():
  api_url = 'https://maps.googleapis.com/maps/api/place/search/json?keyword=coffee&location=40.642696,-73.930595&radius=100&sensor=false&key=AIzaSyBvTCnjwofaUqzwma6gtWOyJIqTNOTStGg'
  # api_url = 'https://yahoo.com'
  # api_url = 'http://news.com.au'
  for i in range(10):
    urls = []
    for url in range(50):
      urls.append(api_url)
    yield from process_batch_of_urls(i, urls)

loop = asyncio.get_event_loop()
connector = aiohttp.TCPConnector(share_cookies=True, loop=loop)
loop.run_until_complete(process_all())
