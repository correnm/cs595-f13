import bottle
from bottle import route, run, template, response
import json
from ordereddict import OrderedDict

from getTopsy import getTopsyCreationDate
from getBitly import getBitlyCreationDate
from getArchives import getArchivesCreationDate
from getGoogle import getGoogleCreationDate
from getBacklinks import *
from getLowest import getLowest
from getLastModified import getLastModifiedDate
# Corren: added this import statement
import simplejson

#---------------------------------------------------------------------------------------#
#--------------------------Server Section-----------------------------------------------#
#---------------------------------------------------------------------------------------#

# Corren: Removed this statement
#@route("/cd/:url#.+#")
def index(url):
	response.content_type = 'application/json; charset=UTF-8'
	print"\n--- Getting Creation dates for:\n"+url+"\n"

	bitly = getBitlyCreationDate(url)
	print "Done Bitly"
	archives = getArchivesCreationDate(url)
	print "Done Archives"
	topsy = getTopsyCreationDate(url)
	print "Done Topsy"
	google = getGoogleCreationDate(url)
	print "Done Google"
	backlink = getBacklinksFirstAppearanceDates(url)
	print "Done Backlinks"
	lastmodified = getLastModifiedDate(url)
	print "Done Last Modified"
	lowest = getLowest([bitly,topsy,google,backlink,lastmodified,archives["Earliest"]])
	print "Got Lowest"

	result = []
	result.append(("URI", url))
	result.append(("Estimated Creation Date", lowest))
	result.append(("Last Modified", lastmodified))
	result.append(("Bitly.com", bitly))
	result.append(("Topsy.com", topsy))
	result.append(("Backlinks", backlink))
	result.append(("Google.com", google))
	result.append(("Archives", archives))
	values = OrderedDict(result)
	#Corren: changed json call to simplejson due to runtime error
	r = simplejson.dumps(values, sort_keys=False, indent=2, separators=(',', ': '))
	print r
	#Corren: extract the just desired element
	createDate=values['Estimated Creation Date']
	return createDate
 
bottle.debug(True) 
fileConfig = open("config", "r")
config = fileConfig.read()
fileConfig.close()
json = simplejson.loads(config)

#Corren: Removed since we are using a file input not a web service
#ServerIP = json["ServerIP"]
#ServerPort = json["ServerPort"]
#run(host=ServerIP, port=int(ServerPort))
