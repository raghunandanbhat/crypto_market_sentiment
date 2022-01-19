import tweepy
import twitter

def auth_twitter():

    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                            CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)

    #return twitter_api
    twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
    search_results = twitter_stream.statuses.filter(track='#btc -filter:retweets', filter_level='medium')
    for tweet in search_results:
        print(tweet['text'])
        
        
    return twitter_api


if __name__ == "__main__":
    ta = auth_twitter()

