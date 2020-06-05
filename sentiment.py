# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 22:10:44 2019

@author: user
"""
from textblob import TextBlob

def ngrams(input, n):
  input = input.split(' ')
  output = []
  for i in range(len(input)-n+1):
    output.append(input[i:i+n])
    
  return output

#function for sentiment
def sentiment_analysis(tweets):
    tweet_sentiment=[]
    count=1
    for tweet in tweets:
        if(TextBlob(tweet).sentiment.polarity>0):
            sentiment="positive"
        elif(TextBlob(tweet).sentiment.polarity<0):
            sentiment="negative"
        else:
            sentiment="neutral"
       # temp['text'] =tweet
        #temp['sentiment']=sentiment
        tweet_sentiment.append({"text":tweet,"sentiment":sentiment})
        print("sentiment calculated to tweet no ",count)
        count=count+1
    return tweet_sentiment


#function for sentiment splitting
def pos_neg_neu_percent(tweet_sentiment,length):
    tweet_percent=[]
    ptweets = [tweet for tweet in tweet_sentiment if tweet['sentiment'] == 'positive'] 
    ptweetsPercentage = 100*len(ptweets)/length
    ntweets = [tweet for tweet in tweet_sentiment if tweet['sentiment'] == 'negative'] 
    ntweetsPercentage = 100*len(ntweets)/length
    neutweetsPercentage = (100-ptweetsPercentage-ntweetsPercentage)
    tweet_percent = { "positive":ptweetsPercentage,
                      "negative":ntweetsPercentage,
                      "neutral":neutweetsPercentage
                    }
    return tweet_percent
