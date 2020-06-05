# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 21:05:23 2019

@author: user
"""
from core.preprocessing.tweet_preprocessing import(
        preprocess,
        translate_to_telugu,
        translate_to_english,
        telugu_tweet_to_english)
from core.extraction.tweet_extraction import (
        twitter_setup,
        readTweetFromCSV)
from core.extraction.livetweets import(
        live_tweets)
from core.analisys.sentiment import (
        sentiment_analysis,
        pos_neg_neu_percent,
        ngrams)
from core.visualization.visualization import(
        visualization)
import tweepy           # To consume Twitter's API
import csv              # to perform operations on csv file


consumer_key = "dNLLEPjGMnLxFXFTbPV1d7uXn"
consumer_secret = "cvH7BisG8u3khjpH8CoUt9ODpTRukRC35z07ks91nS4ziN792W"
access_token = "1017464608431341568-ah98Q1Gp7weFiKYb8S4FHYhhKOyyhg"
access_secret = "jI2F1EiO7kxxmT52BcKJW0wo7fBx3qjb4btrfkIUYwE4P"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

eng_tweets=r"data\eng_tweets.csv"
tel_tweets=r"data\tel_tweets.csv"
query="tdp"
count=20

#------------------------------------------------------------------------------
# created twitter api:
extractor = twitter_setup(consumer_key,consumer_secret,access_token,access_secret)
eng_searched_tweets = [status.text for status in tweepy.Cursor(extractor.search, q=query,lang='en').items(count)]
tel_searched_tweets = [status.text for status in tweepy.Cursor(extractor.search, q=query,lang='te').items(count)]

#------------------------------------------------------------------------------
#write extracted tweets into csv files
with open(eng_tweets, "w", encoding='utf-8') as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in eng_searched_tweets:
        writer.writerow([val])
with open(tel_tweets, "w", encoding='utf-8') as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in tel_searched_tweets:
        writer.writerow([val])

live_tweets(auth)
   
#------------------------------------------------------------------------------
#read tweets from csv file
english_tweets=readTweetFromCSV(eng_tweets)
telugu_tweets=readTweetFromCSV(tel_tweets)

#------------------------------------------------------------------------------
#preprocessing of english tweets
print("\nPreprocessing of english tweets started:\n Removing Special Charecters...")
eng_tweets_with_alphanum = preprocess(english_tweets)
print("\n Removed Special Charecters Successfully")
print("------------------------------------------------------------------------------")

print("\nTranslating English Tweets to Telugu...")
eng_to_tel_tweet = translate_to_telugu(eng_tweets_with_alphanum)
print("\nSuccessfully Translated English to Telugu")
print("------------------------------------------------------------------------------")

print("\nSemantically Translating Telugu Tweet to English...")
translated_english_tweets=translate_to_english(eng_to_tel_tweet)
print("\nSuccessfully Translated Telugu to English")
print("------------------------------------------------------------------------------")

#tel_translated_tweets=telugu_tweet_to_english(tel_searched_tweets)
print("\nPreprocessing of english tweets Done Successfully")
print("------------------------------------------------------------------------------")

#------------------------------------------------------------------------------
#preprocessing of telugu tweets
print("preprocessing of telugu tweets...")
tel_tweets_with_alphanum = preprocess(telugu_tweets)
print("\n Removed Special Charecters Successfully")
print("------------------------------------------------------------------------------")

print("\nSemantically Translating Telugu Tweet to English...")
translated_telugu_tweets=translate_to_english(tel_tweets_with_alphanum)
print("\nSuccessfully Translated Telugu to English")
print("------------------------------------------------------------------------------")

print("\nPreprocessing of telugu tweets Done Successfully")
print("------------------------------------------------------------------------------")

#merging english tweets & telugu tweets
print("merging english & telugu tweets...")
tweets_for_analyze=translated_english_tweets+translated_telugu_tweets
print("merging completed successfully")

#calculating analisys

ngrams_tweets=[]
for tweet in tweets_for_analyze:
    output=""
    sentence=ngrams(tweet, 8)
    for word in sentence:
        output=output+' '+' '.join(word)
    ngrams_tweets.append(output)


print("\nAnalysis started:\n Calculating Polarity...")
tweet_sentiment=sentiment_analysis(ngrams_tweets)
print("\n Polarity Successfully calculated")
print("------------------------------------------------------------------------------")

print("\nCalculating Polarity Percentages--->Positive,Neutral,Negative")
sentiment_percentage=pos_neg_neu_percent(tweet_sentiment,len(english_tweets))
print("\n Polarity Percentages are Successfully Calculated")
print("Analysis Successfully Completed")
print("------------------------------------------------------------------------------")

#visualization
print("\nVisualizing the Sentiment Pi-chart of :",query)
visualization(sentiment_percentage)
print("Sentiment.png is Successfully Saved to \images Directory")