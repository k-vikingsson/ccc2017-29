import analyse_tweets as at
import tweet_locator as tl
import json
import couchdb

if __name__ == '__main__':
	print('start transfer')
	server = couchdb.Server('http://cloud:password@115.146.93.125:5984')
	db = server['tweets_with_sentiment']
	target = server['final_tweets']
	# target = server['tiny_tweet_with_sentiment']
	for id in db:
		tweet = db[id]
		tweet_json = json.dumps(tweet)
		tweet_json = json.loads(tweet_json)
		city = find_city(tweet_json)
		if city == None: continue
		sent_score = at.get_sentiment_score(tweet_json['text'])
		emojis = at.get_emojis(tweet_json['text'])
		tweet_json['_id'] = tweet_json['id_str']
		tweet_json['sentiment'] = sent_score
		tweet_json['emojis'] = emojis
		tweet_json['sa3_city'] = city
		target.save(tweet_json)


