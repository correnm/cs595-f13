from twitter import *
import csv

def extractLinks():
    CONSUMER_KEY = "LrA1DdH1QJ5cfS8gGaWp0A"
    CONSUMER_SECRET = "9AX14EQBLjRjJM4ZHt2kNf0I4G77sKsYX1bEXQCW8"

    OAUTH_TOKEN = "1862092890-FrKbhD7ngeJtTZFZwf2SMjOPwgsCToq2A451iWi"
    OAUTH_TOKEN_SECRET = "AdMQmyfaxollI596G82FBipfSMhagv6hjlNKoLYjeg8"

    # Authenticate Twitter access using tokens and keys for @CorrenMcCoy
    t = Twitter(
            auth=OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                       CONSUMER_KEY, CONSUMER_SECRET)
           )
    # Define all the keywords of interest which must be passed URL encoded.
    # Only return/filter tweets that contain links
    #tso.setKeywords(['Putin', 'chemical%20weapons', 'Kerry', 'Russia', 'Syria', 'Obama', 'Assad'])
    # we want to see English tweets only'
    #tso.setLanguage('en')
    # maximum number of tweets to return
    #tso.setCount(4)
    # include the entity information
    #tso.setIncludeEntities(true)
    #tso.setResultType('mixed')
    
    # Search Twitter
    for tweet in t.search.tweets(q="#pycon&count=1"):
        print tweet.json()





