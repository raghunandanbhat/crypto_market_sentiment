from matplotlib import pyplot as plt
import numpy as np
import pymongo
import datetime
import clean_tweets as ct
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#connect to mongo db to get stored tweets
try:
    client = pymongo.MongoClient("mongodb+srv://username:password@cluster0.lsras.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["crypto_mmi"]
    #collection tweet 
    tweet_collection = db["tweets"]
    #tweet_collection = db["test"]
    mmi_collection = db["mmi_by_date"]
    #print(db)
except:
    print("Couldn't establish database connection")

def get_data_from_db():
    
    start = datetime.datetime(2021, 12, 6, 00, 00, 00)
    end = datetime.datetime(2021, 12, 7, 00, 00, 00)
    tweet_cursor = tweet_collection.find({"created_at": {"$gte":start, "$lt":end}})
    return tweet_cursor

def get_sentiment():
    pos_count = 0
    neg_count = 0
    neu_count = 0

    tweets = get_data_from_db()
    analyser = SentimentIntensityAnalyzer()

    for tweet in tweets:
        tweet_text = ct.clean_tweets(tweet['full_text'])

         #get sentiment from VADER
        senti = analyser.polarity_scores(tweet_text)

        if senti['compound']< -0.5:
            neg_count += 1
        elif senti['compound'] > 0.5:
            pos_count += 1
        else:
            neu_count += 1

    lables = ['posotive', 'negative', 'neutral']

    print(lables)
    print(pos_count, neg_count, neu_count)
    senti_set = [pos_count, neg_count,neu_count]

    fig = plt.figure(figsize=(5,2.5))

    plt.bar(lables, senti_set, color='blue', width = 0.4)
    plt.xlabel("Sentiments")
    plt.ylabel("No. of tweets")
    plt.title("Tweets distribution")
    plt.show()

    return

if __name__ == '__main__':
    get_sentiment()

