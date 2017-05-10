from nltk.tokenize import word_tokenize
from sklearn.feature_extraction import DictVectorizer
import sentiment_classifier as sc
import codecs
import json
import re
import csv

vectorizer, classifier = sc.train_classifier()
with codecs.open('emojis.csv','r','utf-8') as emoji_file:
    emojis = []
    while True:
        line = emoji_file.readline()
        if line == '': break
        else: emojis.append(line.split(',')[0])

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
tweet = '\U0001f601,eye | face | grin | smile'
 
def tokenize(s):
    return word_tokenize(s)
    #return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def prepare_text(text):
	bow = {}
	for token in text:
		bow[token] = bow.get(token, 0) + 1
	return [bow]

def get_emojis(tweet):
    tweet = tokenize(tweet)
    emoji_in_tweet = ''
    for token in tweet:
        for emoji in emojis:
            if emoji in token:
                emoji_in_tweet += token
                break
    return emoji_in_tweet

#    for i in emojis:
#        if i in tweet: continue
#        else: print 'Found', i
	

def get_sentiment_score(text):
    text = preprocess(text, True)
    text = sc.replace_emoji(text)
    text = sc.remove_stop(text)
    filtered = []
    for token in text:
        if not token.isalpha(): continue
        filtered.append(token)
    t_bow = prepare_text(filtered)
    t_vec = vectorizer.transform(t_bow)
    # take the score as the probability of the tweet being positive
    return classifier.predict_proba(t_vec)[0][1]

if '__name__' == '__main__':
    texts = []
    filtered = []

    with open('tweets-26th-April.txt') as datafile:
    	for line in datafile:
    		if line[0] == '{':
    			text = json.loads(line)['text']
    			texts.append(preprocess(text, True))

    for text in texts:
        new = []
        text = sc.replace_emoji(text)
        text = sc.remove_stop(text)
        for token in text:
            if not token.isalpha(): continue
            new.append(token)
        filtered.append(new)


    vectorizer, classifier = sc.train_classifier()

    for text in filtered:
        t_bow = prepare_text(text)
        t_vec = vectorizer.transform(t_bow)
        p_class = classifier.predict(t_vec)
        p_prob = classifier.predict_proba(t_vec)
        print(text, p_class, p_prob)
