from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import couchdb
import json

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '857238507345002496-AAjnTPj2X0sVs331Va7hzNXtZY9gwkb'
ACCESS_SECRET = 'VQaNtQhEguRrtcl2Y8UJUAeMb5eKWuXcrCw3ttYmZkpOy'
CONSUMER_KEY = 'xyMSt6qisWFd1F2UsevzqE6vh'
CONSUMER_SECRET = 'f0GSnExhl6EMpcHYxAUt3CajPWSJyWdX4Bs96SzRBYwJ78Hwnq'
SERVER = couchdb.Server("http://cloud:password@115.146.93.125:5984")
DB = SERVER['tweets']

class StdOutListener(StreamListener):

    def on_data(self, data):
        DB.save(json.loads(data))
        print str(json.loads(data))
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    stream = Stream(auth, l)

    stream.filter(locations=[112,-44,154,-9])
