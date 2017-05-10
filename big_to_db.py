import analyse_tweets as at
import json
import couchdb
from shapely.geometry import Polygon
from shapely.geometry import Point

def find_city(tweet, places):
	try:
		x = tweet['coordinates']['coordinates'][0]
		y = tweet['coordinates']['coordinates'][1]
		for (bounds, name) in places:
			for bound in bounds:
				poly = Polygon(bound)
				point = Point(x, y)
				if poly.contains(point):
					return name
		return None
	except: return None

if __name__ == '__main__':
	server = couchdb.Server('http://cloud:password@115.146.93.125:5984')
	db = server['final_tweets']

	with open('SA3_AU_16.js') as shapes_file:
		shapes = json.load(shapes_file)
		locales = [(place['geometry']['coordinates'],place['properties']) for place in shapes['features']]

	places = []
	for (shapes, name) in locales:
		place_bounds = []
		for shape in shapes:
			shape_bound = []
			if len(shape) == 1: shape = shape[0]
			for coords in shape:
				shape_bound.append((coords[0], coords[1]))
			place_bounds.append(tuple(shape_bound))
		places.append((place_bounds, name))

	print 'start reading'
	with open('bigTwitter.json') as tweets_file:
		for line in tweets_file:
			if line[0] == '{':
				tweet = json.loads(line.strip(',\n'))
				tweet_json = tweet['json']
				city = find_city(tweet_json, places)
				if city == None: continue
				sent_score = at.get_sentiment_score(tweet_json['text'])
				emojis = at.get_emojis(tweet_json['text'])
				tweet_json['_id'] = tweet_json['id_str']
				tweet_json['sentiment'] = sent_score
				tweet_json['emojis'] = emojis
				tweet_json['sa3_city'] = city
				try: db.save(tweet_json)
				except: continue


