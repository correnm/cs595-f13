\begin{verbatim}
from __future__ import division
from math import sqrt
import sqlite3

'''
@Author Corren McCoy, 2013
@Purpose
Item and user-based recommendations using logic
from textbook "Programming Collective Intelligence"
'''

# A dictionary of movie critics and their ratings of a small
# set of movies (sample dataset)
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

conn = sqlite3.connect("mydatabase.db") # or use :memory: to put it in RAM
cursor = conn.cursor()
  
# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
  # Get the list of shared_items
  si={}
  for item in prefs[person1]: 
    if item in prefs[person2]: si[item]=1

  # if they have no ratings in common, return 0
  if len(si)==0: return 0

  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                      for item in prefs[person1] if item in prefs[person2]])
  ## Changed per errata for page 11
  # return 1/(1+sum_of_squares)
  return 1/(1+sqrt(sum_of_squares))

# Returns the Pearson correlation coefficient for p1 and p2
## Changed per errata corrected version found here:
## http://stackoverflow.com/a/13562198/1828663 

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
  # Get the list of mutually rated items
  si={}
  for item in prefs[p1]: 
    if item in prefs[p2]: si[item]=1

  # if they are no ratings in common, return 0
  if len(si)==0: return 0

  ## Changed per errata page 13
  # Sum calculations
  n=float(len(si))
  
  # Sums of all the preferences
  sum1=sum([prefs[p1][it] for it in si])
  sum2=sum([prefs[p2][it] for it in si])
  
  # Sums of the squares
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	
  
  # Sum of the products
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
  
  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0

  r=num/den

  return r

# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]

## Returns the worst matches for person from the prefs dictionary. 
## Number of results and similarity function are optional params.
def worstMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]
  scores.sort()
  return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)

    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:
	    
      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item]==0:
        # Similarity * Score
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim
        # Sum of similarities
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings

def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      
      # Flip item and person
      result[item][person]=prefs[person][item]
  return result


def calculateSimilarItems(prefs,n=10):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  result={}
  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    # Status updates for large datasets
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # Find the most similar items to this one
    # Changed to use Pearson
    #scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_pearson)
    result[item]=scores
  return result

def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # Loop over items rated by this user
  for (item,rating) in userRatings.items( ):

    # Loop over items similar to this one
    for (similarity,item2) in itemMatch[item]:

      # Ignore if this user has already rated this item
      if item2 in userRatings: continue
      # Weighted sum of rating times similarity
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating
      # Sum of all the similarities
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  # Divide each total score by total weighting to get an average
  rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

  # Return the rankings from highest to lowest
  rankings.sort( )
  rankings.reverse( )
  return rankings

def loadMovieLens(path='C:/Python27/myFiles/Assignment 8/data/movielens', insert="N"):
  # Get movie titles
  movies={}
  for line in open(path+'/u.item'):
   (movieid,title)=line.split('|')[0:2]
   movies[movieid]=title
   mi=str(unicode(movieid)).encode('UTF-8')
   mt=str(unicode(title)).encode('UTF-8')
   if insert=="Y":
     # insert some data (movie_id, movie_title)
     cursor.execute("INSERT INTO uitem VALUES (?,?)", (mi, mt))

  
  # Load the ratings
  prefs={}
  for line in open(path+'/u.data'):
    (user,movieid,rating,ts)=line.split('\t')
    prefs.setdefault(user,{})
    prefs[user][movies[movieid]]=float(rating)
    if insert=="Y":
      # insert data (user_id, movie_id, rating)
      cursor.execute("INSERT INTO udata VALUES (?,?,?)", (user, movieid, float(rating)))

  # Load the user demographics
  users={}
  for line in open(path+'/u.user'):
    (user,age,gender,occupation, zip_code)=line.split('|')
    if insert=="Y":
      # insert data (user_id, age, gender)
      cursor.execute("INSERT INTO uuser VALUES (?,?,?)", (user, age, gender))


  # save data to database
  conn.commit()
  return prefs

## Maintain u.data in a database so we can use SQL queries
def openSQL():
  try:
    # create tables(s)
    cursor.execute("""CREATE TABLE udata
                  (
                  user_id integer, movie_id integer, rating integer 
                   ) 
               """)
    # Catch the exception
  except Exception as e:
      print e, "Deleting all rows"
      cursor.execute("""DELETE from udata""")
      conn.commit()
  try:  
    cursor.execute("""CREATE TABLE uitem
                  (
                  movie_id integer, movie_title text
                   ) 
               """)
  # Catch the exception
  except Exception as e:
     print e, "Deleting all rows"
     cursor.execute("""DELETE from uitem""")
     conn.commit() 
  try:   
     cursor.execute("""CREATE TABLE uuser
                  (
                  user_id integer, age integer, gender text) 
               """)
  # Catch the exception
  except Exception as e:
    print e, "Deleting all rows"
    cursor.execute("""DELETE from uuser""")
    conn.commit()
    
def mostAgreed(userset):
  rankings={}
  for user, rating in userset.items():
    difference=0
    for value, key in rating[0:4]:
      # Difference between top four scores and me (4)
      difference= difference + (1-value)
    rankings[user]=difference
  # Return the top 5 rankings from smallest to highest
  count=0
  print "These user ratings most agreed"
  for key, value in sorted(rankings.iteritems(), key=lambda (k,v): (v,k)):
    if (count < 5):
      print key, userset[key][0:4], value
      #print "%s: %s" % (key, value)
    count = count + 1
  return rankings

def mostDisagreed(userset):
  rankings={}
  stop=len(userset)
  start=stop-5
  for user, rating in userset.items():
    difference=0
    for value, key in rating[start:stop]:
      # Difference between bottom four scores and me (4)
      difference= difference + (1-value)
    rankings[user]=difference
  # Return the top 5 rankings from smallest to highest
  count=0
  print "These user ratings most disagreed"
  for key, value in sorted(rankings.iteritems(), key=lambda (k,v): (v,k),reverse=True):
    if (count < 5):
      print key, userset[key][start:stop], value
      #print "%s: %s" % (key, value)
    count = count + 1
  return rankings
## Main driver added
if __name__ == "__main__":
  # Open database connection. Create tables.
  openSQL()	

  # user-based similarity
  print "Calculating user-based similarity"
  userprefs=loadMovieLens(insert="Y")
  moviesim=calculateSimilarItems(userprefs,n=1682) # total number of movies
  print "Calculating item-based similarity"
  
  # item based similarity
  movieprefs=transformPrefs(userprefs)
  usersim=calculateSimilarItems(movieprefs,n=943) # total number of users

  # Which 5 most agreed
  usersA=mostAgreed(usersim)
  usersD=mostDisagreed(usersim)
\end{verbatim}