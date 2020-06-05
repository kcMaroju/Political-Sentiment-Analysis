

from core.preprocessing.tweet_preprocessing import(
        preprocess,
        translate_to_telugu,
        translate_to_english,
        telugu_tweet_to_english)
from core.extraction.tweet_extraction import (
        twitter_setup,
        readTweetFromCSV)
#from core.extraction.livetweets import(
#        live_tweets)
from utils.image_downloader import download_image
from utils.text_extraction_wiki import get_wiki_text
from core.analisys.sentiment import (
        sentiment_analysis,
        pos_neg_neu_percent,
        ngrams)
from core.visualization.visualization import(
        visualization)

from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    url_for,
    jsonify
)

from werkzeug import secure_filename
import os
import tweepy           # To consume Twitter's API
import csv              # to perform operations on csv file

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path='/static')

from logging import Formatter, FileHandler
handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)

consumer_key = "eFTZAd9u4YfHTQTGWX6X1Cea1"
consumer_secret = "vUFdyHTyF5UQhqUZZKov3rWz5nWvFZVvv9eYmOnG4L942bDohz"
access_token = "1017464608431341568-Dh8VL5rWIRhI4B3TVmkxUpzjsnw3bE"
access_secret = "Gj6NBLwnWz1ECsnQCLEs0FjDHVyCSrc2Rakl5fpTY6L4k"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

#eng_tweets=r"data\eng_tweets.csv"
#tel_tweets=r"data\tel_tweets.csv"

query="tdp"
count=20

app.logger.addHandler(handler)

app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'js_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/js', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    elif endpoint == 'css_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/css', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/uploadajax', methods=['POST'])
def upldfile():
    #if request.method == 'POST':
    query = request.form.get('politician_names')
    try:
        print("\nDownloading Image for :",query)
        image_path = download_image(query)
        path = image_path[query][0]
        display_image = path.split('static')[1].replace('\\','/')
        print("\nSuccessfully Downloaded Image",display_image)
        print("------------------------------------------------------------------------------")
        print("Getting text from wikipedia",query)
        
        wiki_text = get_wiki_text(query)
        print("Successfully Extracted Text for:", query)
    
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
    
        eng_tweets=r"data\eng_tweets.csv"
        tel_tweets=r"data\tel_tweets.csv"
    		#query="tdp"
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
        #for tweet in tweets_for_analyze:
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
        sentiment_image = visualization(sentiment_percentage)
        print("Sentiment.png is Successfully Saved to static\images Directory : ", sentiment_image)
    
    except Exception as ex:
        wiki_text = "No Data Available"
        sentiment_image =" "
        display_image = " "
        print(ex)    
        print("Unable to download data.",ex)
    return jsonify(query=query, display_image=display_image, wiki_text=wiki_text, sentiment_image=sentiment_image)


if __name__ == '__main__':
    app.run(debug = True, use_reloader=True)