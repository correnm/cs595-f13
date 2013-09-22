from TwitterSearch import *

try:
    tso = TwitterSearchOrder()
    tso.setKeywords(['Putin', 'chemical%20weapons', 'Kerry', 'Russia', 'Syria', 'Obama', 'Assad'])

    ts = TwitterSearch(
        consumer_key = 'LrA1DdH1QJ5cfS8gGaWp0A',
        consumer_secret = '9AX14EQBLjRjJM4ZHt2kNf0I4G77sKsYX1bEXQCW8',
        access_token = '1862092890-FrKbhD7ngeJtTZFZwf2SMjOPwgsCToq2A451iWi',
        access_token_secret = 'AdMQmyfaxollI596G82FBipfSMhagv6hjlNKoLYjeg8'
     )


    # init variables needed in loop
    todo = True
    next_max_id = 0

    # let's start the action
    while(todo):

        # first query the Twitter API
        response = ts.searchTweets(tso)

        # print rate limiting status
        #print "Current rate-limiting status: %i" % rs.getMetadata()['x-rate-limit-reset']

        # check if there are statuses returned and whether we still have work to do
        todo = not len(response['content']['statuses']) == 0

        # check all tweets according to their ID
        for tweet in response['content']['statuses']:
            tweet_id = tweet['id']
            print("Seen tweet with ID %i" % tweet_id)

            # current ID is lower than current next_max_id?
            if (tweet_id < next_max_id) or (next_max_id == 0):
                next_max_id = tweet_id
                next_max_id -= 1 # decrement to avoid seeing this tweet again

        # set lowest ID as MaxID
        tso.setMaxID(next_max_id)

except TwitterSearchException as e:
    print(e)
