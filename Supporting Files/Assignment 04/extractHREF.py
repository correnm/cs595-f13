\begin{verbatim}
#!/usr/bin/python
from BeautifulSoup import BeautifulSoup
import codecs
import os
import sys
import time
import urllib2
import urllib
import urlparse
import unicodedata

'''
Given a file of URIs, extract all user-navigable links from the web page.
Create a "dot" file in the GraphViz format using
the URI and the title associated with the "<a href=. . .>" tag.
Author:  Corren McCoy, 2013
'''

# Initialize global variables
baseFileName = 'C:/Python27/myFiles/Assignment 4/output/file'    
dotFileName  = 'C:/Python27/myFiles/Assignment 4/gephi/twitter.dot'
fileLimit = 100
fileCounter = 0
# Initialize the dot file
graphviz = codecs.open(dotFileName, 'w', 'utf-8')

   
def extractHREF(url):
    global baseFileName
    # Prepare the output file for this URL
    currentFileName = baseFileName + str(fileCounter) + '.txt'
    currentFile = codecs.open(currentFileName,'w','utf-8')

                               
    # Write the header for the URI file
    currentFile.write('site:\n')
    currentFile.write(url + '\n')
    currentFile.write('links:')
                      
    # package the request
    try:
        request=urllib2.Request(url)
        request.add_header('User-agent','Mozilla 5.10')
        response=urllib2.urlopen(request)
        if response.code == 200:
            html=response.read()
            # decode byte stream to unicode
            html = html.decode("utf-8")
            # encode to ASCII byte stream, removing characters with codes >127
            html = html.encode("ascii", "ignore") 
            soup = BeautifulSoup(html)
        response.close()

        # create an empty dictionary. We want to build a dictionary {uri: {link:[title]}}
        site={}
        links={}
        numLinks=0
        # Extract information from the anchor tag
        for tag in soup.findAll('a', href=True):
            tag['href'] = urlparse.urljoin(url, tag['href'])
            tld = tag['href']
            # Outbound links only. Must not have the same top-level domain
            # Ignore javascript in anchor tag (e.g. javascript:void(0)
            if tld.find(url) == -1 and tld.find("javascript") == -1: 
                title=  str(tag.string).strip()
                # components for the dictionary
                links[tag['href']]= title
                site[url] = links
            # Verification: Keep track of the number of original links encountered
            numLinks = numLinks + 1
        # Iterate over the full URI dictionary.
        # The links will be unique, unduplicated    
        for siteKey, linkValue in site.iteritems():
            for link, title in linkValue.iteritems():
                currentFile.write('\n')
                currentFile.write(link)
                # add the node to Graphviz file
                graphviz.write('\n')
                graphviz.write('"' +siteKey+'"' + '->' + '"' + link + '" ' 
								+ ' [label="' + title + '"];')
            # Verification. Compare original to unduplicated number of key-value pairs. 
            print(siteKey, "Unduplicated:", len(links), "Full URI Count", str(numLinks))
        # Done with this URI
        currentFile.close()

    except urllib2.HTTPError,e:
        print "Error", url, e
        return
    except urllib2.URLError, e:
        print "Error", url, e
        return
    except IOError, e:
        print "Error", url, e
        return
    except UnicodeDecodeError, e:
        print "Error", url, e
        return
    
############################################################################             
#  This is main procedure in this package
############################################################################
def main():
    print "Press Control-C to exit"
    #continue until Control-C is entered from keyboard

    # The tweet file contains our 1000 URIs
    fileObject = open('C:/Python27/myFiles/Assignment 4/tweetFile1000.txt','r')

    # Extract links from 100 pages
    uriFile = open('C:/Python27/myFiles/Assignment 4/tweetFile1000.txt').readlines()
		[1:fileLimit]
    # Write the header
    graphviz.write("digraph twitter { \n")
    graphviz.write('size="6,6"; \n')
    graphviz.write('node [color=lightblue2, style=filled];');
                           
    for line in fileObject.readlines():
        try:
            global fileCounter
            fileCounter = fileCounter+1

            # Remove the final newline character
            url = line.rstrip('\n')
            # Processing is limited to 100 files
            if fileCounter > fileLimit:
                break
            print "Processing file", fileCounter
            extractHREF(url)
            # Raised when the user hits the interrupt key (normally Control-C or Delete).

        except KeyboardInterrupt:
            print ""
            print "processing terminated."
            sys.exit(0)
    # close the Tweek file               
    fileObject.close()
    # close the Graphviz dot file
    graphviz.write("\n}")
    graphviz.close()
    print ">>>>File processing complete"

\end{verbatim}