#!/usr/bin/python -B
import urllib2
import urllib
import codecs
import re

# Save the final count to a comma delimited file
def saveToFile(pUri, pCount):
    # append the data
    histogram = codecs.open('C:/Python27/myFiles/histogram.txt','a','utf-8')
    histogram.write(pUri + ',' + str(pCount) + '\n')
    histogram.close()
    
def countMementos(pUri, pTimeMap):
    # Re-use from regular expressions from Scott's timeMap.py
    tokenizer = re.compile('(<[^>]+>|[a-zA-Z]+="[^"]*"|[;,])\\s*')
    mementoCount=0
    # The timeMap is passed as a string. Read/split each line
    for line in pTimeMap.splitlines():
        # Parse the line into tokens to find what's in the rel= tag
        tokens=tokenizer.findall(line)
        for x in tokens:
            # Find the token using Scott's logic from timeMap.py
            if x[:4] == 'rel=':
                rel=x[5:-1]
                # if "memento" is anywhere in the rel tag, let's count it
                if rel.find('memento') <> -1:
                    mementoCount = mementoCount + 1
        
    # This will be a number >= 0
    saveToFile(pUri, mementoCount)

############################################################################             
#  This is main function in this package
############################################################################
   
'''
Invoke the ODU Memento Aggregator for each of our 1000 unique
Twitter links.  Search the resulting timeMaps, if any, for valid mementos
which are identified as any valid combination of:
    rel="memento"
    rel="first memento"
    rel="last memento"
    rel="memento first"
    rel="memento last"
    rel="first last memento"
'''
def findMementos():
    # Base setting for the aggregator
    uriBase="http://mementoproxy.cs.odu.edu/aggr/timemap/link/"
    notInArchive=0
    
    # Write the header of our histogram data file
    histogram = codecs.open('C:/Python27/myFiles/histogram.txt','w','utf-8')
    histogram.write("uri" + "," + "mementos" + "\n")
    histogram.close()
    
    # Open the file containing our 1000 links from Twitter
    tweetFile = open('C:/Python27/myFiles/tweetFile1000.txt')
    lineNo=0
    for line in iter(tweetFile):
        lineNo=lineNo+1  # for checking progress of iteration over URIs
        uri=line.rstrip('\n')
        # Package the request. Append the target uri to complete.
        uri_t=uriBase+uri
        print lineNo, uri_t
        # Search for any timeMaps
        try:
            request=urllib2.Request(uri_t)
            response=urllib2.urlopen(request)
            if response.code==200:
                timeMap=response.read()
                # Parse out the string we're looking for.
                # Record the URI and the count in a file.
                # The file will be used later to create a Histogram in R
                countMementos(uri, timeMap)
            response.close()
        except urllib2.HTTPError,e:
            print "Error", e
            # A 404 response from aggregator indicates "Resource not in archive"
            saveToFile(uri, notInArchive)
            continue
        except urllib2.URLError, e:
             print "Error", e
             continue
        except IOError, e:
             print "Error", e
             continue
    # Done processing. Close the file.       
    tweetFile.close()
    print ">>> Session Complete. . ."
