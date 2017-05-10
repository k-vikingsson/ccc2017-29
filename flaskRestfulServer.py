from flask import Flask, jsonify, request
import socket
import json
from couchdbViewManager import CouchdbViewManager

app = Flask(__name__)
couchdbVM = CouchdbViewManager()


@app.route('/')
def index():
    str = 'Team 29 <br /> \
           /views/city_average_sentiment <br />\
           /views/city_language <br />\
           /views/emoji_contains_smile <br />\
           /views/hours_average_sentiment <br />\
           /views/tweets_city_eng_noneng <br />\
           /views/weekday_average_sentiment <br />\
           /views/aurin_city_eng_noneng <br /> \
           /views/person_earn_2000_vic <br /> '
    return str


@app.route("/views/city_average_sentiment")
def get_city_average_sentiment():
    try:
        f = open('./city_average_sentiment.json')
    except IOError:
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str

@app.route("/views/city_language")
def get_city_language():
    try:
        f = open('./city_language.json')
    except IOError:
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/views/emoji_contains_smile")
def get_emoji_contains_smile():
    try:
        f = open('./emoji_contains_smile.json')
    except IOError:
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/views/hours_average_sentiment")
def get_hours_average_sentiment():
    try:
        f = open('./hours_average_sentiment.json')
    except IOError:
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/views/tweets_city_eng_noneng")
def get_tweets_city_eng_noneng():
    try:
        f = open('./tweets_city_eng_noneng.json')
    except IOError:
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/views/weekday_average_sentiment")
def get_weekday_average_sentiment():
    try:
        f = open('./weekday_average_sentiment.json')
    except IOError:
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/views/aurin_city_eng_noneng")
def get_aurin_city_eng_noneng():
    try:
        f = open('./aurin_city_eng_noneng.json')
    except IOError:
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/views/person_earn_2000_vic")
def get_person_earn_2000_vic():
    try:
        f = open('./person_earn_2000_vic.json')
    except IOError:
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/updateViews")
def updateviews():
    couchdbVM = CouchdbViewManager()
    couchdbVM.save_view("final_tweets", "Scenarios/city_language")
    couchdbVM.save_view("final_tweets", "Scenarios/city_average_sentiment")
    couchdbVM.save_view("final_tweets", "Scenarios/emoji_contains_smile")
    couchdbVM.save_hours_view("final_tweets", "Scenarios/hours_average_sentiment")
    couchdbVM.save_view("final_tweets", "Scenarios/tweets_city_eng_noneng")
    couchdbVM.save_weekday_view("final_tweets", "Scenarios/weekday_average_sentiment")
    couchdbVM.save_view("language", "Scenario/aurin_city_eng_noneng")
    couchdbVM.save_view("person_earn_2000_weekly_vic", "newDoc/person_earn_2000_vic")
    return "Done!"

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    app.run("115.146.93.125", 5000, debug=True)
