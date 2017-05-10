from shapely.geometry import Polygon
from shapely.geometry import Point
import json

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

def find_city(tweet):
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


