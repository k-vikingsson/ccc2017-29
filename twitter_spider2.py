import couchdb
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import json

# run on the local host
server = couchdb.Server('http://cloud:password@115.146.93.125:5984/')
# get the database
db = server["test"]


class StdOutListener(StreamListener):
    def on_data(self, data):
        msg = json.loads(data)
        db.save(msg)
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = tweepy.OAuthHandler("Dyie4i0j4k8C7gOPmZjM4OdJs", "0HowjpFknNVokSeTXCHnUe9Y6YpbPZw44a32sa5qLy27BI0xNc")
    auth.set_access_token("3060113220-D9PNijWjcTu7GFps35V20isvIev9zHYkpGnuhQp",
                          "Ep9MrunK4ORjTCmX3aH3T093fUJ3qAYdxwOIrJbSv1atr")

    stream = Stream(auth, l)

    stream.filter(locations=[112, -44, 154, -9])
