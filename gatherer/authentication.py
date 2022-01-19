import tweepy

#function to authenticate twitter API
def auth_twitter():
    
    consumer_key = ''
    consumer_secret = ''
    accessToken = ''
    accessTokenSecret = ''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(accessToken, accessTokenSecret)

    twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
    #stream = tweepy.Stream(consumer_key, consumer_secret,accessToken,accessTokenSecret)
    #print(stream)

    return twitter_api

#if __name__ == "__main__":
#    ta = auth_twitter()

