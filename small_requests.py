import requests as r

url = 'https://maps.googleapis.com/maps/api/place/search/json?keyword=coffee&location=40.638878,-73.967525&radius=100&sensor=false&key=AIzaSyBvTCnjwofaUqzwma6gtWOyJIqTNOTStGg'
for x in range(0,1000):
	c = r.get(url)
	if c.status_code == 200:
		print("pass")
	else:
		print("fail")