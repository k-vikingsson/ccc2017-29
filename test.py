#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-03 18:05:35
# @Author  : Jinchao Cai
# @Link    : http://example.org
# @Version : $Id$

import os
import re
import sys
import codecs
from nltk.tokenize import TweetTokenizer, word_tokenize


if __name__ == '__main__':
    emotionList = []
    with codecs.open('emojis.csv', 'r', 'utf-8') as f:
        while True:
            line = f.readline()
            if line == '':
                break
            else:
                emotionList.append(line.split(',')[0])
    print(emotionList)
    tweet = "Sunset view of #Sydney yesterday from @watsonsbayhotei . So beautiful 😍😍 #travel #fbloggers #pretty… http://t.co/rr95NRvQZB"
    words = word_tokenize(tweet)
    print(words)
    for word in words:
        for emoji in emotionList:
            if emoji in word:
                print(emoji + 'Yes')
# file_path = '/Users/Jinchao/Desktop/2017S1-KTproj2-data/train-tweets.txt'
# if len(sys.argv) < 2:
#     pass
# else:
#     file_path = sys.argv[1]
# tweet_data = []
# with codecs.open(file_path, 'r', 'utf-8') as f:
#     while True:
#         line = f.readline()
#         if line == '':
#             break
#         else:
#             tweet_data.append(line)
# tweet_label = {}
# label_path = '/Users/Jinchao/Desktop/2017S1-KTproj2-data/train-labels.txt'
# with codecs.open(label_path, 'r', 'utf-8') as f:
#     while True:
#         line = f.readline()
#         if line == '':
#             break
#         else:
#             tmp = line.split()
#             tweet_label[tmp[0]] = tmp[1]
# for x in range(1, len(tweet_data)):
#     if tweet_label[tweet_data[x][0:18]] != None:
#         tweet_data[x] = tweet_data[x][18:-2] +\
#             tweet_label[tweet_data[x][0:18]][0:3]
# result = []
# for x in range(1, len(tweet_data)):
#     if tweet_data[x].endswith('neu'):
#         pass
#     else:
#         result.append((tweet_data[x][1:-4], tweet_data[x][-3:]))
# # for x in range(1, len(result)):
# #     print(result[x])
# print(result)
# pattern = re.compile(
#     '\\\\x[0-9a-z][0-9a-z]\\\\x[0-9a-z][0-9a-z]\\\\x[0-9a-z][0-9a-z]\\\\x[0-9a-z][0-9a-z]')
# match = pattern.match('\\xf5\\xg7\\xt9\\xf1\\x7h\\x7h\\x7h\\x7h')
# match = pattern.match('\\xf5\\xg7')
# print(match)
