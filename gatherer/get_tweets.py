from logging import NullHandler
import tweepy
import datetime
import authentication as auth
import clean_tweets as ct
import pymongo
import json


class TwitterStream(tweepy.Stream):

    def on_status(self, status):
        #print(status.id, status.text)
        tweet_count = 0
        if not status.retweeted and 'RT @' not in status.text:
            mined = {
                "tweet_id": status.id,
                "created_at": status.created_at,
                "mined_at": datetime.datetime.now(),
                "name": status.user.name,
                "screen_name": status.user.screen_name,
                "full_text": status.text,
                "hashtags": [i.get('text').lower() for i in status.entities["hashtags"]],
                "retweet_count": status.retweet_count,
                "favourite_count": status.favorite_count,
                "followers_count": status.user.followers_count
            }
            print(mined)
            if insert_to_db(mined):
                tweet_count += 1


#connect to mongo db
try:
    client = pymongo.MongoClient("mongodb+srv://rgbhat:Tf.xZ4WSThB.7QX@cluster0.lsras.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["crypto_mmi"]
    #collection tweet 
    tweet_collection = db["tweets"]
    #tweet_collection = db["test"]
except:
    print("Couldn't establish database connection")

#function to insert data to mongodb database
def insert_to_db(mined):
    try:
        id = tweet_collection.update_one(mined, {"$set":mined}, upsert=True)
    except pymongo.errors.DuplicateKeyError:
        return None
    return id

#function to get tweets based on the search terms mentioned in the tweets
def get_tweets_by_hashtags(tag):
    
    #twitter API authentication
    twitter_api = auth.auth_twitter()
    #twitter_stream = auth.auth_twitter()

    #search term with hashtag and filter out retweets to eliminate retrival of duplicat tweets
    search_term = tag+' -filter:retweets'
    #print(search_term) result_type='popular',
    
    #Cursor to get the tweets page by page 
    for page in tweepy.Cursor(twitter_api.search_tweets, q=search_term, lang='en', count=100).pages(10):
        
        tweet_count = 0
        #take each item in a page and mine tweets
        for item in page:            
        #collect only tweet text, retweet count, favourite_count, etc...    
            mined = {
                "tweet_id": item.id,
                "created_at": item.created_at,
                "mined_at": datetime.datetime.now(),
                "name": item.user.name,
                "screen_name": item.user.screen_name,
                #get full text of the tweets
                #"text": twitter_api.get_status(item.id, tweet_mode = "extended").full_text,
                "full_text": twitter_api.get_status(item.id, tweet_mode = "extended").full_text,
                "hashtags":[i.get('text').lower() for i in item.entities["hashtags"]],
                "retweet_count": item.retweet_count,
                "favourite_count": item.favorite_count,
                "followers_count": item.user.followers_count
            }
            #print(mined)

            #insert mined tweets to db
            if insert_to_db(mined):
                tweet_count += 1
        
        
    print('Collected {} tweets for {}'.format(tweet_count,tag))


def get_tweets():

    #to instanciate the streaming API class of Tweepy
    consumer_key = ''
    consumer_secret = ''
    accessToken = ''
    accessTokenSecret = ''

    #considering top 10 cryptocurrencies by marekt value
    hash_tags = [
        "#crypto",
        "#cryptocurrency",
        "#bitcoin",
        "#btc",
        "#ethereum",
        "#eth",
        "#binance",
        "#bnb",
        "#tether",
        "#usdt",
        "#cardano",
        "#ada",
        "#solana",
        "#sol",
        "#ripple",
        "#xrp", 
        "#polkadot",
        "#dot",
        "#shibainu",
        "#shib",
        "#dogecoin",
        "#doge"
    ]

    #get_tweets_by_hashtags("#btc")
    for tag in hash_tags:
        print("Mining tweets for {}...".format(tag))
        get_tweets_by_hashtags(tag)

    # ONLY TO BE USED IF DATA VOLUME AVAILABLE IS LESS
    '''
    #create Twitter Stream object
    twitter_stream = TwitterStream(consumer_key, consumer_secret,accessToken,accessTokenSecret)
    #Filter tweets using Streaming API 
    twitter_stream.filter(track=hash_tags, languages=["en"])
    '''    
    pass

if __name__ == "__main__":
    get_tweets()