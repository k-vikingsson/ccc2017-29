from nltk.corpus import stopwords
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score
import nltk
import numpy as np
import scipy
import csv

positive_tweets = nltk.corpus.twitter_samples.tokenized("positive_tweets.json")
negative_tweets = nltk.corpus.twitter_samples.tokenized("negative_tweets.json")
stopwords = stopwords.words('english') # stopwords to be filtered
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

with open('emojis.csv') as emoji_csv:
    emojis = {}
    reader = csv.reader(emoji_csv)
    for emoji, text in reader:
        emojis[emoji] = text
    emoji_set = set(emojis.keys())

def replace_emoji(tweet):
    returned = []
    for word in tweet:
        if word in emoji_set:
            returned.append(emojis[word])
        else: returned.append(word)
    return returned

# Function to filter tokens of stopwords 
# or containing non-alphabetical characters.
def filter_tweets(tweets):
    filtered_tweets = []
    for i in range(len(tweets)):
        filtered = []
        tweet = tweets[i]
        tweet = replace_emoji(tweet)
        for j in range(len(tweet)):
            if tweet[j] in stopwords: continue
            if tweet[j].isalpha():
                filtered.append(tweet[j])
        filtered_tweets.append(filtered)
    return filtered_tweets

def remove_stop(sentence):
    new = []
    for word in sentence:
        if not word in stopwords:
            new.append(word)
    return new

# Get Bag Of Word from given list of tokens.
# Reused from WSTA_N2_text_classification.ipynb 
def get_BOW(text):
    BOW = {}
    for token in text:
        BOW[lemmatize(token)] = BOW.get(lemmatize(token),0) + 1
    return BOW

# Prepare tweets to be processed by classifiers.
# Partially reused from WSTA_N2_text_classification.ipynb 
def prepare_tweet_data(tweets, feature_extractor):
    feature_matrix = []
    for i in range(len(tweets)):
        feature_dict = feature_extractor(tweets[i])
        feature_matrix.append(feature_dict)
    return feature_matrix

# Function to lemmatize a word.
# Reused from WSTA_N1B_preprocessing.ipynb
def lemmatize(word):
    lemma = lemmatizer.lemmatize(word,'v')
    if lemma == word:
        lemma = lemmatizer.lemmatize(word,'n')
    return lemma

def train_classifier():
    filtered_pos_tweets = filter_tweets(positive_tweets)
    filtered_neg_tweets = filter_tweets(negative_tweets)

    all_tweets = filtered_pos_tweets + filtered_neg_tweets
    feature_matrix = prepare_tweet_data(all_tweets, get_BOW)

    vectorizer = DictVectorizer()
    dataset = vectorizer.fit_transform(feature_matrix)

    pos_tweets = dataset[range(len(positive_tweets))]
    neg_tweets = dataset[range(len(negative_tweets), len(all_tweets))]

    classes = np.empty(dataset.shape[0])
    classes.fill(0)
    for i in range(pos_tweets.shape[0]):
        classes[i] = 1

    # Build classifiers with best settings found in previous step.
    mnnb = MultinomialNB(2, False, None)

    # Train classifiers.
    mnnb.fit(dataset, classes)
    return vectorizer, mnnb






