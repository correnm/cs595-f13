\begin{verbatim}
# TwitterSearch package obtained from https://github.com/ckoepp/TwitterSearch

from TwitterSearch import *
import codecs
import urllib
import urllib2
from urlparse import urlparse


# This function iterates over the twitter entity object to
# find a particular element
def posted_url(dictionary):
    # Recursively iterates over entities to find expanded URLs
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
           posted_url(value)
        else:
           return(value)

# Save the final list of 1000 unique links
def saveToFile(pLinks):
    linkFile = codecs.open('C:/Python27/myFiles/linkFile.txt','w','utf-8')
    for key in pLinks:
        linkFile.write(key+'\n');
    
# This function searches Twitter for a particular keyword
def searchTwitter(pThisTerm):
 try:
    # create a TwitterSearchOrder object
    tso = TwitterSearchOrder()
    # Define all the keywords which must be passed URL encoded.
    # Only return/filter tweets that contain links
    tso.setKeywords(["filter%3Alinks",pThisTerm]) 
    # we want to see English tweets only'
    tso.setLanguage('en')
    # maximum number of tweets to return
    tso.setCount(100)
    # include the entity information
    tso.setIncludeEntities(True)
    #tso.setResultType('recent')

    # create a TwitterSearch object with my secret tokens (@CorrenMcCoy)
    ts = TwitterSearch(
        consumer_key = 'LrA1DdH1QJ5cfS8gGaWp0A',
        consumer_secret = '9AX14EQBLjRjJM4ZHt2kNf0I4G77sKsYX1bEXQCW8',
        access_token = '1862092890-FrKbhD7ngeJtTZFZwf2SMjOPwgsCToq2A451iWi',
        access_token_secret = 'AdMQmyfaxollI596G82FBipfSMhagv6hjlNKoLYjeg8'
     )

    # Iterate over the tweet entities which are in a nested dictionary
    tweetFile = codecs.open('C:/Python27/myFiles/tweetFile.txt','a','utf-8')
    for tweet in ts.searchTweetsIterable(tso): 
        #print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
        if tweet['user']['url'] is not None:
            print (tweet['user']['url'])
            tweetFile.write(tweet['user']['url']+'\n');

    tweetFile.close()

 # Error handling. Close file and terminate
 except TwitterSearchException as e:
    tweetFile.close()
    print(e)
    exit()

def findUniqueLinks():
    tweetFile = open('C:/Python27/myFiles/tweetFile.txt')
    # initialize the list to hold all the fully expanded URIs
    # that respond with 200
    tweetURLs=[]
    # create an empty dictionary
    domains={}
    for line in iter(tweetFile):
        uri = line.rstrip('\n')
        #package the request
        request=urllib2.Request(uri)
        request.add_header('User-agent','Mozilla 5.10')
        try:
            response=urllib2.urlopen(request)
            if response.code == 200:
                tweetURLs.append(response.url)
                # make sure there's only one URI with the same domain.
                # http://stackoverflow.com/questions/10362453/unique-by-domains-urls-list
                # Return the last URL for each domain the URL list. By definition, the key
                # in a dictionary is unique.
                domains=dict((urlparse(u).netloc, u) for u in tweetURLs).values()

                # Stop traversing the file when we reach the 1000th domain
                if len(domains)== 1000:
                    # Write out the URLS so we can use them for other tasks
                    saveToFile(domains)
                    return
            print response.code,response.url, "Domains=", len(domains)
            response.close()
        except urllib2.HTTPError,e:
            print "Error", line, e
            continue
        except urllib2.URLError, e:
            print "Error", line, e
            continue
        except IOError, e:
            print "Error", line, e
            continue
    # how many links do we have?
    print "Unique links = ", len(domains)
    tweetFile.close()


############################################################################             
#  This is main procedure in this package
############################################################################
def extractLinks():
    # Use these keywords to build a list of Tweets from which we will extract
    # the desired 1000 unique links.
    keywordList={"Putin","Syria","Assad","Obama","chemical%20weapons"}
    for thisTerm in keywordList:
        print "Tweets for keyword>>>",thisTerm    
        searchTwitter(thisTerm)
    print "Twitter search complete>>>>>>"
    
    # Read the file of links.
    findUniqueLinks()
    print "1000 links saved to file>>>>>"
\end{verbatim}