\begin{verbatim}
'''
@Author Corren McCoy, 2013
@Purpose
Use the Twitter APIs to extract:
(1) the followers (count) of a certain user including the followers 
of those entities
(2) the following (count) of a certain user including the number of 
accounts his followers are following.
(3) the friends (count) of a certain user include the number friends 
associated with his followers
Note:  The Twitter API indicates that following is otherwise known as their "friends"

Example request:
https://api.twitter.com/1.1/followers/list.json? 
+ cursor=-1&screen_name=sitestreams&skip_status=true&include_user_entities=false

This code leverages tweepy (https://code.google.com/p/tweepy/) which is
a Python API for twitter. It provides a nice wrapper for the Twitter APIs
'''
import tweepy
import time

# Initialize the oAuth authentication settings
# Documentation: https://dev.twitter.com/docs/auth/oauth
CONSUMER_KEY = "LrA1DdH1QJ5cfS8gGaWp0A"
CONSUMER_SECRET = "9AX14EQBLjRjJM4ZHt2kNf0I4G77sKsYX1bEXQCW8"
OAUTH_TOKEN = "1862092890-FrKbhD7ngeJtTZFZwf2SMjOPwgsCToq2A451iWi"
OAUTH_SECRET = "AdMQmyfaxollI596G82FBipfSMhagv6hjlNKoLYjeg8"

# Dr. Nelson's twitter account
USERNAME='phonedude_mln'
# variables used to manage the API rate limit
FIFTEEN_MIN=900 # seconds
FIVE_MIN=300

# first set up authenticated API instance
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
#create an instance of a tweepy StreamListener to handle the incoming data
api = tweepy.API(auth, api_root='/1.1')

# open the output file that will contain the data for graphing in "R"
followersFile = open('C:/Python27/myFiles/Assignment 5/followersFile.txt','w')
# write the header line for identification
followersFile.write("ID" +"," +"COUNT" + "," + "FOLLOWER.USERNAME" )

try:
    counter = 0
    for follower in tweepy.Cursor(api.followers, screen_name=USERNAME).items():
            counter = counter + 1
            print follower.screen_name, follower.followers_count
            followersFile.write('\n')
            followersFile.write(str(counter) +',' + str(follower.followers_count) 
            +',' + follower.screen_name)
            
            # Returns the remaining number of API requests available to the requesting user
            # before the API limit of 180 requests every 15 minutes
            # Calls to rate_limit_status do not count against the rate limit.
            remaining_hits = api.rate_limit_status('application')['resources']['application']
            ['/application/rate_limit_status']['remaining']
           
            if (remaining_hits < 5):# or counter % 160 == 0:
                print '\n' 
                print 'You have', remaining_hits, 'API calls remaining in this window. 
                Started sleeping at', time.ctime() 
                time.sleep(FIFTEEN_MIN)
            else:
                pass
    followersFile.close()
    print '\n'
    print 'You have', remaining_hits, 'API calls remaining in this window.', time.ctime()
   
except tweepy.error.TweepError as e:
    print e.reason
    followersFile.close()
\end{verbatim}