\begin{verbatim}
'''
@Author Corren McCoy, 2013
@Purpose
Use the Twitter APIs to extract:
(1) the friends (count) of a certain user including the friends of those entities
(2) the following (count) of a certain user including the number of accounts 
his followers are following.

Example request:
https://api.twitter.com/1.1/followers/list.json?cursor=-1
+ &screen_name=sitestreams&skip_status=true&include_user_entities=false

This code leverages tweepy (https://code.google.com/p/tweepy/) which is a 
Python API for twitter. It provides a nice wrapper for the Twitter APIs
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

## first set up authenticated API instance
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
#create an instance of a tweepy StreamListener to handle the incoming data
api = tweepy.API(auth, api_root='/1.1')

# open the output file that will contain the data for graphing in "R"
friendFile = open('C:/Python27/myFiles/Assignment 5/friendsFile.txt','w')
# write the header line for identification
friendFile.write("ID" + "," + "COUNT" +"," + "FOLLOWING.USERNAME")

try:
    counter = 0
    for friend in tweepy.Cursor(api.friends, screen_name=USERNAME).items():
            counter = counter + 1
            print friend.screen_name, friend.friends_count
            friendFile.write('\n')
            friendFile.write(str(counter) +',' + str(friend.friends_count)+ ',' + 
            friend.screen_name)
            
            # Returns the remaining number of API requests available to the requesting user
            # before the API limit is reached for the current hour.
            # Calls to rate_limit_status do not count against the rate limit.
            remaining_hits = api.rate_limit_status('application')['resources']['application']
            ['/application/rate_limit_status']['remaining']
            #remaining_hits=api.rate_limit_status['remaining_hits']

            if (remaining_hits < 5): #or counter % 160 == 0:
                print '\n' 
                print 'You have', remaining_hits, 'API calls remaining in this window. 
                Started sleeping at', time.ctime() 
                time.sleep(FIFTEEN_MIN)
            else:
                pass
    friendFile.close()
    print '\n'
    print 'You have', remaining_hits, 'API calls remaining in this window.', time.ctime()
    
except tweepy.error.TweepError as e:
    print e.reason
    friendFile.close()
\end{verbatim}