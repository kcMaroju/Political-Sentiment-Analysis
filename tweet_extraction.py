# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 21:09:25 2019

@author: user
"""

import tweepy
import pandas as pd

# API's setup:
def twitter_setup(consumer_key,consumer_secret,access_token,access_secret):
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret) 

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

def readTweetFromCSV(eng_tweets):
    tweets=pd.read_csv(eng_tweets,lineterminator='\n',header=None)
    return tweets[0].tolist()