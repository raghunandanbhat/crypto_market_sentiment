import re

#dictionary of contractions 
# Source: https://en.wikipedia.org/wiki/Contraction_%28grammar%29
contractions = {
        "ain't":"is not",
        "amn't":"am not",
        "aren't":"are not",
        "can't":"cannot",
        "'cause":"because",
        "couldn't":"could not",
        "couldn't've":"could not have",
        "could've":"could have",
        "daren't":"dare not",
        "daresn't":"dare not",
        "dasn't":"dare not",
        "didn't":"did not",
        "doesn't":"does not",
        "don't":"do not",
        "e'er":"ever",
        "em":"them",
        "everyone's":"everyone is",
        "finna":"fixing to",
        "gimme":"give me",
        "gonna":"going to",
        "gon't":"go not",
        "gotta":"got to",
        "hadn't":"had not",
        "hasn't":"has not",
        "haven't":"have not",
        "he'd":"he would",
        "he'll":"he will",
        "he's":"he is",
        "he've":"he have",
        "how'd":"how would",
        "how'll":"how will",
        "how're":"how are",
        "how's":"how is",
        "I'd":"I would",
        "I'll":"I will",
        "I'm":"I am",
        "I'm'a":"I am about to",
        "I'm'o":"I am going to",
        "isn't":"is not",
        "it'd":"it would",
        "it'll":"it will",
        "it's":"it is",
        "I've":"I have",
        "kinda":"kind of",
        "let's":"let us",
        "mayn't":"may not",
        "may've":"may have",
        "mightn't":"might not",
        "might've":"might have",
        "mustn't":"must not",
        "mustn't've":"must not have",
        "must've":"must have",
        "needn't":"need not",
        "ne'er":"never",
        "o'":"of",
        "o'er":"over",
        "ol'":"old",
        "oughtn't":"ought not",
        "shalln't":"shall not",
        "shan't":"shall not",
        "she'd":"she would",
        "she'll":"she will",
        "she's":"she is",
        "shouldn't":"should not",
        "shouldn't've":"should not have",
        "should've":"should have",
        "somebody's":"somebody is",
        "someone's":"someone is",
        "something's":"something is",
        "that'd":"that would",
        "that'll":"that will",
        "that're":"that are",
        "that's":"that is",
        "there'd":"there would",
        "there'll":"there will",
        "there're":"there are",
        "there's":"there is",
        "these're":"these are",
        "they'd":"they would",
        "they'll":"they will",
        "they're":"they are",
        "they've":"they have",
        "this's":"this is",
        "those're":"those are",
        "'tis":"it is",
        "'twas":"it was",
        "wanna":"want to",
        "wasn't":"was not",
        "we'd":"we would",
        "we'd've":"we would have",
        "we'll":"we will",
        "we're":"we are",
        "weren't":"were not",
        "we've":"we have",
        "what'd":"what did",
        "what'll":"what will",
        "what're":"what are",
        "what's":"what is",
        "what've":"what have",
        "when's":"when is",
        "where'd":"where did",
        "where're":"where are",
        "where's":"where is",
        "where've":"where have",
        "which's":"which is",
        "who'd":"who would",
        "who'd've":"who would have",
        "who'll":"who will",
        "who're":"who are",
        "who's":"who is",
        "who've":"who have",
        "why'd":"why did",
        "why're":"why are",
        "why's":"why is",
        "won't":"will not",
        "wouldn't":"would not",
        "would've":"would have",
        "y'all":"you all",
        "you'd":"you would",
        "you'll":"you will",
        "you're":"you are",
        "you've":"you have",
        "Whatcha":"What are you",
        "luv":"love",
        "sux":"sucks"
        }

def clean_tweets(tweet):
    
    #convert all text to lowercase to maintain uniformity of text
    #tweet = tweet.lower()

    #remove hastgas
    tweet = ' '.join(re.sub("#[a-zA-Z0-9]+", " ", tweet).split())

    #remove username mentions in tweets starting with @
    tweet = ' '.join(re.sub("@[a-zA-Z0-9]+", " ", tweet).split())

    '''
    #get all crypto ticker symbols in tweet
    ticker_symbols = re.findall("\$[a-zA-Z]+", tweet)
    #remove tickers from the tweets
    tweet = ' '.join(re.sub("\$[a-zA-Z0-9]+", " ", tweet).split())'''
    
    #remove links in tweets
    tweet = ' '.join(re.sub("(\w+:\/\/\S+)", " ", tweet).split())
    #print(tweet)

    #remove special characters
    tweet = ' '.join(re.sub('[$%&.,|=+-]', '', tweet).split())
    #print(tweet)

    #remove digits
    tweet = ' '.join(re.sub('[0-9]', '', tweet).split())
    tweet = ' '.join(re.sub('\n', ' ', tweet).split())

    # replace contractions with full words using the contractions dict
    #tweet = tweet.replace("’","'")
    #print(tweet)
    words = tweet.split()
    extended = [contractions[word]  if word in contractions else word for word in words]
    tweet = ' '.join(extended)

    return tweet

'''
if __name__ == "__main__":
    #tweet = '$SHIB Building for the reversal when crypto starts running again. Been buying under .00004s \n\n#SHIB #ShibaCoin #ShibaSwap #SHIBARIUM #Shiboshis #SHIBUSDT #ShibainuCoin $BTC $ETH $LTC $DOGE $HOOD $COIN #bitcoin   #etherium #ETH #BTC #LTC https://t.co/VdyiGorwdI'
    pass
    '''