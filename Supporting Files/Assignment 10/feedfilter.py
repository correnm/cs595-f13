\begin{verbatim}
import feedparser
import re
import math

# Takes a filename or URL of a blog feed and classifies the entries
def read(feed,classifier):
  num=0
  # Get feed entries and loop over them
  f=feedparser.parse(feed)
  print
  print '----- Begin manual classification (training) -----'
  for entry in f['entries'][0:50]:
    num=num +1
    # Print the contents of the entry
    title=entry['title'].encode('utf-8').replace("'","")
    print 'Title:     '+ title
    #print entry['summary'].encode('utf-8')

    # Combine all the text to create one item for the classifier
    #fulltext='%s\n%s\n%s' % (entry['title'],entry['publisher'],entry['summary'])
    fulltext='%s\n%s' % (entry['title'],entry['summary'])
    # Remove apostrophes
    fulltext=fulltext.replace("'","")
    # Print the best guess at the current category
    predicted=str(classifier.classify(fulltext))
    print 'Predicted category: ', predicted

    # Ask the user to specify the correct category and train on that
    actual=raw_input('Actual category: ')
    feature=None
    classifier.train(fulltext, actual)
 
    # Save the manual classifications
    # num, entry, feature, predicted, actual, cprob=None
    classifier.manualClassdb(num, title, feature, predicted, actual)
  
#def autoClassify(feed,classifier):
  num=50
  print '----- Begin automatic classification -----'
  # Get feed entries and loop over them
  f=feedparser.parse(feed)
  for entry in f['entries'][51:100]:
    num=num+1
    # Print the contents of the entry
    title=entry['title'].encode('utf-8').replace("'","")
    print 'Title:     '+ title
    #print entry['summary'].encode('utf-8')

    # Combine all the text to create one item for the classifier
    #fulltext='%s\n%s\n%s' % (entry['title'],entry['publisher'],entry['summary'])
    fulltext='%s\n%s' % (entry['title'],entry['summary'])
    fulltext=fulltext.replace("'","")
    # Print the best guess at the current category
    predicted=str(classifier.classify(fulltext))
    print 'Predicted: ', predicted

    # Ask the user to specify the correct category
    actual=raw_input('Enter actual category: ')
    feature=raw_input('Enter string classifier: ')

    #classifier.train(entry,cl)
    # probability the item should be in this category
    cp=round(classifier.cprob(feature,predicted),3)
    print 'cprob: ', str(cp)
    # Save the trained classifications
    # num, entry, feature, predicted, actual, cprob(feature, predicted)
    classifier.autoClassdb(num, title, feature, predicted, actual, cp)    
  #return classifier

def entryfeatures(entry):
  splitter=re.compile('\\W*')
  f={}
  
  # Extract the title words and annotate
  titlewords=[s.lower() for s in splitter.split(entry['title']) 
          if len(s)>2 and len(s)<20]
  for w in titlewords: f['Title:'+w]=1
  
  # Extract the summary words
  summarywords=[s.lower() for s in splitter.split(entry['summary']) 
          if len(s)>2 and len(s)<20]

  # Count uppercase words
  uc=0
  for i in range(len(summarywords)):
    w=summarywords[i]
    f[w]=1
    if w.isupper(): uc+=1
    
    # Get word pairs in summary as features
    if i<len(summarywords)-1:
      twowords=' '.join(summarywords[i:i+1])
      f[twowords]=1
    
  # Removed: Keep creator and publisher whole
  #f['Publisher:'+entry['publisher']]=1

  # UPPERCASE is a virtual word flagging too much shouting  
  if float(uc)/len(summarywords)>0.3: f['UPPERCASE']=1
  
  return f
\end{verbatim}