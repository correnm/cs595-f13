import urllib2
def ScoreTracker():
 response=urllib2.urlopen('http://www.cs.odu.edu/')
 html=response.read()
 print "View Source: ", html
 response.close()
