import couchdb
import json

server = couchdb.Server('http://cloud:password@115.146.93.125:5984')
db = server['tweets']

filename = 'tweets.json'

with open(filename) as data_file:
	for line in data_file:
		if line[0] == '{':
			db.save(json.loads(line))
