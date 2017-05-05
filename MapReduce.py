import couchdb
import json

server = couchdb.Server('http://cloud:password@115.146.93.125:5984/')
#db = server["test"]
#results = db.view('myDesignDoc/test', group=True)

file = open('file.json', 'w', encoding='utf-8')
db = server["tweets_with_sentiment"]

results = db.view('testDoc/countLang', group=True)
for row in results:
    key = row.key
    value = row.value
    data = {"key": str(key), "value": value}
    in_json = json.dumps(data)
    print(in_json)
    file.writelines(in_json + ',\n')

file.close()
