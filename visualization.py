# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 23:17:31 2019

@author: user
"""
import matplotlib.pyplot as plt 
import os
import time
#visualization
def visualization(tweet_percentage):
    labels = list(tweet_percentage.keys())
    sizes = list(tweet_percentage.values())
    explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Positive Tweets')
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
    shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H%M', t)
    sentiment_image = ("sentiment_" + timestamp + ".png")
    #plt.savefig(r'static\images\'sentiment.png')
    plt.savefig(os.path.join('static\img\/' + sentiment_image))
    return sentiment_image
    