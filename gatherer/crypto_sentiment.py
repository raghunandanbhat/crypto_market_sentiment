import pymongo
import datetime as datetime
import clean_tweets as ct
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



#connect to mongo db to get stored tweets
try:
    client = pymongo.MongoClient("mongodb+srv://user_name:password@cluster0.lsras.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["crypto_mmi"]
    #collection tweet 
    tweet_collection = db["tweets"]
    #tweet_collection = db["test"]
    mmi_collection = db["mmi_by_date"]
    #print(db)
except:
    print("Couldn't establish database connection")

#function to insert data to mongodb database
def insert_mmi_to_db(mmi_by_date):
    try:
        id = mmi_collection.update_one(mmi_by_date, {"$set":mmi_by_date}, upsert=True)
    except pymongo.errors.DuplicateKeyError:
        return None
    return True

#get the data for a date range
def get_data_from_db(date):
    
    
    start = date - datetime.timedelta(days=1)#datetime.datetime(2021, 12, 6, 00, 00, 00)
    end = date #datetime.datetime(2021, 12, 7, 00, 00, 00)

    #get data for the given date
    tweet_cursor = tweet_collection.find({"created_at": {"$gte":start, "$lt":end}})
    return tweet_cursor

def get_sentiment_of_tweet(date):

    #analyser from VADER
    analyser = SentimentIntensityAnalyzer()

    mmi= mmi_btc= mmi_eth= mmi_shib= mmi_doge= mmi_bnb = 0
    tweet_count= tweet_count_btc= tweet_count_eth= tweet_count_shib= tweet_count_doge= tweet_count_bnb = 0
    raw_tweet_count = 0

    #get tweets
    tweets = get_data_from_db(date)

    for tweet in tweets:
        
        #clean tweets
        raw_tweet_count += 1
        tweet_text = ct.clean_tweets(tweet['full_text'])
        
        #get sentiment from VADER
        senti = analyser.polarity_scores(tweet_text)
        #print(tweet['tweet_id'], senti, )

        # set likes count to 1 if likes are zero and retweet count to 0.5 if retweet count is 0
        if tweet['retweet_count'] == 0:
            tweet['retweet_count'] = 0.5
        
        if tweet['favourite_count'] == 0:
            tweet['favourite_count'] = 1

        print(tweet['tweet_id'], senti, tweet['retweet_count'], tweet['favourite_count'])

        #calculate the weight of the tweet
        tweet_count = tweet_count + (int(tweet['favourite_count'])+2*int(tweet['retweet_count']))

        # calculate MMI as summation of ( weight * sentiment_score )
        if senti['compound']< -0.5:
            mmi = mmi + ( (int(tweet['retweet_count']) * 2 + int(tweet['favourite_count'])) * (1 + senti['compound']))
        elif senti['compound']> 0.5:
            mmi = mmi + ( (int(tweet['retweet_count']) * 2 + int(tweet['favourite_count'])) * ( senti['compound']))

        # calculate MMI for bitcoin
        if "btc" in tweet['hashtags'] or "bitcoin" in tweet['hashtags']:
            #weight of the btc tweet
            tweet_count_btc = tweet_count_btc +  (int(tweet['favourite_count'])+2*int(tweet['retweet_count']))

            if senti['compound']< -0.5:
                mmi_btc = mmi_btc + ( (int(tweet['retweet_count']) * 2 + int(tweet['favourite_count'])) * (1 + senti['compound']))
            elif senti['compound']> 0.5:
                mmi_btc = mmi_btc + ( (int(tweet['retweet_count']) * 2 + int(tweet['favourite_count'])) * ( senti['compound']))

        # calculate MMI for ether
        if "eth" in tweet['hashtags'] or "ethereum" in tweet['hashtags']:
            #weight of the eth tweet
            tweet_count_eth = tweet_count_eth +  (int(tweet['favourite_count'])+2*int(tweet['retweet_count']))

            if senti['compound']< -0.5:
                mmi_eth = mmi_eth + ( (int(tweet['retweet_count']) * 2 + int(tweet['favourite_count'])) * (1 + senti['compound']))
            elif senti['compound']> 0.5:
                mmi_eth = mmi_eth + ( (int(tweet['retweet_count']) * 2 + int(tweet['favourite_count'])) * ( senti['compound']))

        # calculate MMI for binance
        if "bnb" in tweet['hashtags'] or "binance" in tweet['hashtags']:
            #weight of the bnb tweet
            tweet_count_bnb = tweet_count_bnb +  (int(tweet['favourite_count'])+2*int(tweet['retweet_count']))

            if senti['compound']< -0.5:
                mmi_bnb = mmi_bnb + ( (int(tweet['retweet_count']) * 2 + int(tweet['favourite_count'])) * (1 + senti['compound']))
            elif senti['compound']> 0.5:
                mmi_bnb = mmi_bnb + ( (int(tweet['retweet_count']) * 2 + int(tweet['favourite_count'])) * ( senti['compound']))

        # calculate MMI for dogecoin
        if "doge" in tweet['hashtags'] or "dogecoin" in tweet['hashtags']:
            #weight of the doge tweet
            tweet_count_doge = tweet_count_doge +  (int(tweet['favourite_count'])+2*int(tweet['retweet_count']))

            if senti['compound']< -0.5:
                mmi_doge = mmi_doge + ( (int(tweet['retweet_count']) * 2 + int(tweet['favourite_count'])) * (1 + senti['compound']))
            elif senti['compound']> 0.5:
                mmi_doge = mmi_doge + ( (int(tweet['retweet_count']) * 2 + int(tweet['favourite_count'])) * ( senti['compound']))

        # calculate MMI for Shiba-inu
        if "shib" in tweet['hashtags'] or "shibainu" in tweet['hashtags']:
            #weight of the shib tweet
            tweet_count_shib = tweet_count_shib +  (int(tweet['favourite_count'])+2*int(tweet['retweet_count']))

            if senti['compound']< -0.5:
                mmi_shib = mmi_shib + ( (int(tweet['retweet_count']) * 2 + int(tweet['favourite_count'])) * (1 + senti['compound']))
            elif senti['compound']> 0.5:
                mmi_shib = mmi_shib + ( (int(tweet['retweet_count']) * 2 + int(tweet['favourite_count'])) * ( senti['compound']))


    try:
        print("Total tweets analysed: {}".format(raw_tweet_count))
        # MMI
        final_mmi = mmi/tweet_count
        print("Market Mood Index: {} ".format(final_mmi*100))
        
        # btc MMI
        final_mmi_btc = mmi_btc/tweet_count_btc
        print("Market Mood Index for Bitcoin: {} ".format(final_mmi_btc*100))

        # eth MMI
        final_mmi_eth = mmi_eth/tweet_count_eth
        print("Market Mood Index for Ethereum: {} ".format(final_mmi_eth*100))

        # bnb MMI
        final_mmi_bnb = mmi_bnb/tweet_count_bnb
        print("Market Mood Index for Binance: {} ".format(final_mmi_bnb*100))

        # doge MMI
        final_mmi_doge = mmi_doge/tweet_count_doge
        print("Market Mood Index for Dogecoin: {} ".format(final_mmi_doge*100))

        # shib MMI
        final_mmi_shib = mmi_shib/tweet_count_shib
        print("Market Mood Index for Shiba-inu: {} ".format(final_mmi_shib*100))

        #save MMI to database
        mmi_by_date = {
            "date": datetime.datetime.today().replace(hour=00, minute=00, second=00, microsecond=000000),
            "overall": final_mmi,
            "specific":[
                {"cur":"btc", "mmi":final_mmi_btc},
                {"cur":"eth", "mmi":final_mmi_eth},
                {"cur":"bnb", "mmi":final_mmi_bnb},
                {"cur":"doge", "mmi":final_mmi_doge},
                {"cur":"shib", "mmi":final_mmi_shib}
            ]
        }

        #insert to database
        if insert_mmi_to_db(mmi_by_date):
            print("MMI inserted to database...")
    except ZeroDivisionError:
        print("No data for the givn date in database!")
    

if __name__ == "__main__":
#analyser = SentimentIntensityAnalyzer()
    #date = input("Enter the date:")
    date = datetime.datetime.today().replace(hour=00, minute=00, second=00, microsecond=000000)
    get_sentiment_of_tweet(date)