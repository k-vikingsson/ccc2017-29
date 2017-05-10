import couchdb
import json

FILENAME = 'data.json'
DBNAME = 'language'

if __name__ == '__main__':
	server = couchdb.Server('http://cloud:password@115.146.93.125:5984')
	db = server[DBNAME]
	with open(FILENAME) as json_file:
		for json_obj in json.load(json_file)['features']:
			doc = {}
			# js_str = json.dumps(json_obj)
			# print js_str
			doc['SA3_NAME16'] = json_obj['properties']['SA3_NAME11']
			doc['SEO_Persons'] = json_obj['properties']['SEO_Persons']
			doc['SOL_Tol_P'] = json_obj['properties']['SOL_Tot_P']
			db.save(doc)
