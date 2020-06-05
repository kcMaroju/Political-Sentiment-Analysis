# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 21:33:56 2019

@author: user
"""
import re
from googletrans import Translator

#function to remove special charecters
def preprocess(tweets):
    tweets_preprocess=[]
    for tweet in tweets:
        #for k in tweet.split("\n"):
        tweets_preprocess.append((re.sub(r'\W+', ' ', tweet)))
        #print("Removing Special Charecters for Tweet #: ",count)
        #count=count+1
    return tweets_preprocess
#tweets_alphanum=preprocess(tweets)

#call translate after preprocess
def translate_to_telugu(tweets):
    count=1
    translated_text=[]
    for tweet in tweets:
        trans=Translator()
        translated_text.append((trans.translate(tweet, dest='te')).text)
        print("Translating English Tweets to Telugu for Tweet #: ",count)
        count=count+1
    return translated_text
#eng_tel=tw_translate(tweets_alphanum)

def translate_to_english(tweets):
    count=1
    trans_tweet=[]
    for tweet in tweets:
        trans=Translator()
        trans_tweet.append(trans.translate(tweet).text)
        print("Semantically Translating Telugu Tweet to English for Tweet #: ",count)
        count=count+1
    return trans_tweet
#translated_tweets=translate(eng_tel)

#original telugu tweets translation to english
def telugu_tweet_to_english(tweets):
    tel_trans_tweet=[]
    count=1
    for tweet in tweets:
        trans=Translator()
        tel_trans_tweet.append(trans.translate(tweet).text)
        print("translate tel to eng tweet no ",count)
        count=count+1
    return tel_trans_tweet
#tel_translated_tweets=lang_translate(eng_tel)
