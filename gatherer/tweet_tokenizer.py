import nltk

#nltk.download("stopwords")
#nltk.download("wordnet")
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from textblob import TextBlob

stop_words = stopwords.words("english")
tokenizer = TweetTokenizer()
stemmer = nltk.PorterStemmer()
lemmatizer = nltk.WordNetLemmatizer()

def get_tokenized_tweets(tweet):
    
    tokenized_tweet = tokenizer.tokenize(tweet)
    #print(tokenized_tweet)
    words = [stemmer.stem(word) for word in tokenized_tweet if word not in stop_words]

    tokenized_text = " ".join()
    print(tokenized_text)

if __name__ == "__main__":
    tweet = "Budweiser one of the world's biggest beer companies just changed their profile name to beereth What universe am I living in??? This is crazy!"
    get_tokenized_tweets(tweet)