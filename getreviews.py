import urllib2
import json
import csv
import math
import time

# Set the Places API key for your application
AUTH_KEY = 'AIzaSyB9F9VhZDwPctQnoPJdwH0xlIOVgtMdtIs'


place_list = []
with open('data.csv', 'rb') as r: 
	reader = csv.reader(r)
	for x in reader:
		place_list.append(x)

(place_list[0]).append('rating_count')
(place_list[0]).append('rating_score')

count = 0
for item in place_list:
	if count > 0:
		place_list[count].append(str(0.0))
		place_list[count].append(str(0.0))
	count += 1

count = 0
for ref in place_list:
	if count >0:
		REFERENCE = ref[2]
		url =  ('https://maps.googleapis.com/maps/api/place/details/json?reference=%s&sensor=false&key=%s') % (REFERENCE, AUTH_KEY)
	
		attempt = 0
		max_attempts = 5
		while attempt < max_attempts:
			try:
				response = urllib2.urlopen(url)
				attempt = max_attempts
			except:
				print 'Error, pausing then attempting retry'
				time.sleep(5)
				attempt += 1

		# Get the response and use the JSON library to decode the JSON
		json_raw = response.read()
		json_data = json.loads(json_raw)

		# Iterate through the results and print them to the console
		if json_data['status'] == 'OK':
			place = json_data['result']
			if 'reviews' in place.keys(): 

				
				cur_score = 0.0
				score_count = 0.0
				for review in place['reviews']:
					cur_score += review['rating']
					score_count +=1.0
				cur_score = cur_score/score_count
				place_list[count][-2] = str(score_count)
				place_list[count][-1] = str(cur_score)

	count +=1
	print count

with open('data_with_review_count.csv','wb') as f1:
	writer=csv.writer(f1, delimiter=',',lineterminator='\n',)
	for x in place_list:
		writer.writerow(x)