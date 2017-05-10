##
# COMP90024 Cluster and Cloud Computing
# Assignment 2
#
# File name: flaskRestfulServer.py
# Description: A flask web server that supports ReSTful APIs designed to get scenarios data.
# Author: Hangyu Xia
# Last Modified: 5/11/2017
#

from flask import Flask, jsonify, request, abort, make_response
import socket
import json
from couchdbViewManager import CouchdbViewManager

app = Flask(__name__)
couchdbVM = CouchdbViewManager()


@app.route('/')
def index():
    str = 'Team 29 <br /> \
           /views/city_average_sentiment <br />\
           /views/emoji_contains_smile <br />\
           /views/hours_average_sentiment <br />\
           /views/tweets_city_eng_noneng <br />\
           /views/weekday_average_sentiment <br />\
           /views/aurin_city_eng_noneng <br /> \
           /views/person_earn_2000_vic <br /> '
    return str

@app.route('/views')
def menu():
    obj = {
        "resources":["city_average_sentiment",
                     "emoji_contains_smile",
                     "hours_average_sentiment",
                     "tweets_city_eng_noneng",
                     "aurin_city_eng_noneng",
                     "weekday_average_sentiment",
                     "person_earn_2000_vic"]
    }
    return jsonify(json.dumps(obj))

@app.route("/views/city_average_sentiment", methods=['GET'])
def get_city_average_sentiment():
    try:
        f = open('./city_average_sentiment.json')
    except IOError:
        abort(404)
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


'''
@app.route("/views/city_language", methods=['GET'])
def get_city_language():
    try:
        f = open('./city_language.json')
    except IOError:
        abort(404)
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str
'''

@app.route("/views/emoji_contains_smile", methods=['GET'])
def get_emoji_contains_smile():
    try:
        f = open('./emoji_contains_smile.json')
    except IOError:
        abort(404)
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/views/hours_average_sentiment", methods=['GET'])
def get_hours_average_sentiment():
    try:
        f = open('./hours_average_sentiment.json')
    except IOError:
        abort(404)
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/views/tweets_city_eng_noneng", methods=['GET'])
def get_tweets_city_eng_noneng():
    try:
        f = open('./tweets_city_eng_noneng.json')
    except IOError:
        abort(404)
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/views/weekday_average_sentiment", methods=['GET'])
def get_weekday_average_sentiment():
    try:
        f = open('./weekday_average_sentiment.json')
    except IOError:
        abort(404)
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/views/aurin_city_eng_noneng", methods=['GET'])
def get_aurin_city_eng_noneng():
    try:
        f = open('./aurin_city_eng_noneng.json')
    except IOError:
        abort(404)
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/views/person_earn_2000_vic", methods=['GET'])
def get_person_earn_2000_vic():
    try:
        f = open('./person_earn_2000_vic.json')
    except IOError:
        abort(404)
        pass
    callback = request.args.get('callback', False)
    json_str = f.read()
    if callback:
        json_str = callback + '(' + json_str + ')'
    return json_str


@app.route("/updateViews", methods=['GET'])
def updateviews():
    couchdbVM = CouchdbViewManager()
    #couchdbVM.save_view("final_tweets", "Scenarios/city_language")
    couchdbVM.save_view("final_tweets", "Scenarios/city_average_sentiment")
    couchdbVM.save_view("final_tweets", "Scenarios/emoji_contains_smile")
    couchdbVM.save_hours_view("final_tweets", "Scenarios/hours_average_sentiment")
    couchdbVM.save_save_tweets_eng_view("final_tweets", "Scenarios/tweets_city_eng_noneng")
    couchdbVM.save_weekday_view("final_tweets", "Scenarios/weekday_average_sentiment")
    couchdbVM.save_view("language", "Scenario/aurin_city_eng_noneng")
    couchdbVM.save_view("person_earn_2000_weekly_vic", "newDoc/person_earn_2000_vic")
    return "Done!"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    #ip = socket.gethostbyname(socket.gethostname())
    app.run("115.146.93.125", 5000, debug=True)
