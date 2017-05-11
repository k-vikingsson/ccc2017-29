##
## COMP90024 Cluster and Cloud Computing
## Assignment 2
## City: Melbourne
##
## File: tweet_to_couch_with_sentiment.py
## Description: Twitter harvester, tweets are saved to database as document
##              with sentiment value, emojis used and the city of tweet.
##
## Team 29
## Members:
## Name         | Student ID | e-mail
## Hangyu XIA   | 802971     | hangyux@student.unimelb.edu.au
## Hanwei ZHU   | 811443     | hanweiz@student.unimelb.edu.au
## Jinchao CAI  | 838073     | jinchaoc1@student.unimelb.edu.au
## Wenzhuo MI   | 818944     | miw@student.unimelb.edu.au
## Zequn MA     | 696586     | zequnm@dimefox.eng.unimelb.edu.au
##

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import analyse_tweets as at
import tweet_locator as tl
import couchdb
import json
import sys

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '857238507345002496-AAjnTPj2X0sVs331Va7hzNXtZY9gwkb'
ACCESS_SECRET = 'VQaNtQhEguRrtcl2Y8UJUAeMb5eKWuXcrCw3ttYmZkpOy'
CONSUMER_KEY = 'xyMSt6qisWFd1F2UsevzqE6vh'
CONSUMER_SECRET = 'f0GSnExhl6EMpcHYxAUt3CajPWSJyWdX4Bs96SzRBYwJ78Hwnq'


class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet_json = json.loads(data)
        city = tl.find_city(tweet_json)
        if city == None: return True
        sent_score = at.get_sentiment_score(tweet_json['text'])
        emojis = at.get_emojis(tweet_json['text'])
        tweet_json['_id'] = tweet_json['id_str']
        tweet_json['sentiment'] = sent_score
        tweet_json['emojis'] = emojis
        tweet_json['sa3_city'] = city
        try: DB.save(tweet_json)
        except: return True
        # print(tweet_json)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print sys.argc
        print("Usage: python3 harvester.py <couchdb_ip>")
    else: ip_addr = sys.argv[-1]

    SERVER = couchdb.Server("http://cloud:password@" + ip_addr + ":5984")
    # create database if not already exist
    try: DB = SERVER['final_tweets']
    except: DB = SERVER.create('final_tweets')

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    stream = Stream(auth, l)

    stream.filter(locations=[112,-44,154,-9])
