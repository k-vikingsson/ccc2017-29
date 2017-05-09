import analyse_tweets as at
import json
import couchdb

if __name__ == '__main__':
	print('start transfer')
	server = couchdb.Server('http://cloud:password@115.146.93.125:5984')
	db = server['tweets']
	#target = server['']
	target = server['tiny_tweet_with_sentiment']
	for id in db:
		tweet = db[id]
		tweet_json = json.dumps(tweet)
		tweet_json = json.loads(tweet_json)
		sent_score = at.get_sentiment_score(tweet_json['text'])
		emojis = at.get_emojis(tweet_json['text'])
		tweet_json['_id'] = tweet_json['id_str']
		tweet_json['rubbish'] = 'null'
		tweet_json['sentiment'] = sent_score
		tweet_json['emojis'] = emojis
		target.save(tweet_json)


