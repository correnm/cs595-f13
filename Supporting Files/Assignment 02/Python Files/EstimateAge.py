# Utilities from Hany's Carbon Date too
import codecs
import datetime
from server import index

# Initialize the file for our final results
ageFile = codecs.open('C:/Python27/myFiles/Assignment 2/uri_age.txt','w','utf-8')

# Save the URIs, creation date, age
def saveToFile(pURI, pMementos, pCreationDate, pAge):
    ageFile.write(pURI + "," + pMementos +"," + pCreationDate + "," + pAge +'\n');
   

def estimateAge():

    # Today's date
    today=datetime.datetime.now()
    # Write the header line
    ageFile.write("URI" + "," + "Mementos" + "," + "Creation Date" + "," + "Age" +'\n');
    
    # The histogram file contains our 1000 URIs and number of mementos
    # skip the header row: URI, memento
    uriFile = open('C:/Python27/myFiles/Assignment 2/histogram.txt').readlines()[1:]

    fileCounter=0
    for line in uriFile:
        fileCounter=fileCounter+1
        data = line.rstrip('\n')
        # separate comma delimited file into fields
        words={}
        uri=""
        mementos=""
        age=None
        words=data.split(",")
        if len(words) >=2:
            uri=words[0]
            mementos=words[1]
            # for URIs with > 0 mementos, find the estimated creation date
            if int(mementos) > 0:
                # send URI to Carbon Date tool
                est_creation_date=index(uri)
                if est_creation_date != "":
                    delta= today - datetime.datetime.strptime(est_creation_date, '%Y-%m-%dT%H:%M:%S')
                    # convert to days
                    age = str(delta.days)
                    saveToFile(uri, mementos, est_creation_date, age)
        print fileCounter, mementos, uri,est_creation_date, age
    ageFile.close()


