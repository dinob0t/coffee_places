import asyncio
import aiohttp

def main():
	print("here")
	url = 'https://maps.googleapis.com/maps/api/place/search/json?keyword=coffee&location=40.642696,-73.930595&radius=100&sensor=false&key=AIzaSyBvTCnjwofaUqzwma6gtWOyJIqTNOTStGg'
	# url = 'https://yahoo.com'
	for x in range(0,300):
		response = yield from aiohttp.request('GET', url)

		if response.status == 200:
			print("pass %d" % x)
		else:
			print("failed on %d" % x)
			print(response.content, response.status)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())

# Traceback (most recent call last):
#   File "/usr/local/lib/python3.4/site-packages/aiohttp/client.py", line 106, in request
#     conn = yield from connector.connect(req)
#   File "/usr/local/lib/python3.4/site-packages/aiohttp/connector.py", line 135, in connect
#     transport, proto = yield from self._create_connection(req)
#   File "/usr/local/lib/python3.4/site-packages/aiohttp/connector.py", line 242, in _create_connection
#     **kwargs))
#   File "/usr/local/Cellar/python3/3.4.1/Frameworks/Python.framework/Versions/3.4/lib/python3.4/asyncio/base_events.py", line 381, in create_connection
#     infos = f1.result()
#   File "/usr/local/Cellar/python3/3.4.1/Frameworks/Python.framework/Versions/3.4/lib/python3.4/asyncio/futures.py", line 243, in result
#     raise self._exception
#   File "/usr/local/Cellar/python3/3.4.1/Frameworks/Python.framework/Versions/3.4/lib/python3.4/concurrent/futures/thread.py", line 54, in run
#     result = self.fn(*self.args, **self.kwargs)
#   File "/usr/local/Cellar/python3/3.4.1/Frameworks/Python.framework/Versions/3.4/lib/python3.4/socket.py", line 530, in getaddrinfo
#     for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
# socket.gaierror: [Errno 8] nodename nor servname provided, or not known

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "small_async.py", line 18, in <module>
#     loop.run_until_complete(main())
#   File "/usr/local/Cellar/python3/3.4.1/Frameworks/Python.framework/Versions/3.4/lib/python3.4/asyncio/base_events.py", line 208, in run_until_complete
#     return future.result()
#   File "/usr/local/Cellar/python3/3.4.1/Frameworks/Python.framework/Versions/3.4/lib/python3.4/asyncio/futures.py", line 243, in result
#     raise self._exception
#   File "/usr/local/Cellar/python3/3.4.1/Frameworks/Python.framework/Versions/3.4/lib/python3.4/asyncio/tasks.py", line 319, in _step
#     result = coro.send(value)
#   File "small_async.py", line 9, in main
#     response = yield from aiohttp.request('GET', url)
#   File "/usr/local/lib/python3.4/site-packages/aiohttp/client.py", line 118, in request
#     raise aiohttp.OsConnectionError(exc)
# aiohttp.errors.OsConnectionError: [Errno 8] nodename nor servname provided, or not known
