# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 19:16:44 2019

@author: user
"""
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from core.preprocessing.tweet_preprocessing import(
        preprocess,
        translate_to_telugu,
        translate_to_english,
        telugu_tweet_to_english)



#consumer key, consumer secret, access token, access secret.
ckey="dNLLEPjGMnLxFXFTbPV1d7uXn"
csecret="cvH7BisG8u3khjpH8CoUt9ODpTRukRC35z07ks91nS4ziN792W"
atoken="1017464608431341568-ah98Q1Gp7weFiKYb8S4FHYhhKOyyhg"
asecret="jI2F1EiO7kxxmT52BcKJW0wo7fBx3qjb4btrfkIUYwE4P"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        count=1
        eng_tweets_with_alphanum = preprocess(tweet)
        #print(tweet)
        print("Removing Special Charecters for Tweet #: ",count)
        count=count+1
        
        return eng_tweets_with_alphanum

    def on_error(self, status):
        print(status)



auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

def live_tweets(auth):
    twitterStream = Stream(auth, listener())
    return twitterStream.filter(track=["tdp"])
    
live_tweets(auth)