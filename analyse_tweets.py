from nltk.tokenize import word_tokenize
from sklearn.feature_extraction import DictVectorizer
import sentiment_classifier as sc
import json
import re

vectorizer, classifier = sc.train_classifier()

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:\\\\x[a-z0-9][a-z0-9]\\\\x[a-z0-9][a-z0-9]\\\\x[a-z0-9][a-z0-9]\\\\x[a-z0-9][a-z0-9])',
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
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

 
# tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
# print(preprocess(tweet))

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
        print text, p_class, p_prob
