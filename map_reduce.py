import couchdb
from couchdb.design import ViewDefinition
from textblob import TextBlob

server = couchdb.Server('http://cloud:password@115.146.93.125:5984/')
db = server['test']


map_fun = """function(doc){
   emit([doc.place.name,doc.lang], 1);
  }
"""

red_fun = """function(keys,values,rereduce){
    return sum(values);
  }
"""

'''
#python map_function
def map_fun(doc):
    yield doc["text"], doc["user"]["lang"]
'''

#define a view
view = ViewDefinition('myDesignDoc', 'test', map_fun, red_fun)
#syschronize the view in database with this view
view.sync(db)
#d = view.get_doc(db)
#execute the view named test in myDesignDoc and store the results in results
results = db.view("myDesignDoc/test", group=True)
for item in results:
    print(item)

