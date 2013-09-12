#!/usr/bin/python
from BeautifulSoup import BeautifulSoup
import os
import sys
import time
import urllib2
import urllib
def teamSelectionMenu():
    #Display menu until user selects a valid option
    while True:
        #Use an associative array to store the team names and menu options.
        #The values (team names) must match how the names are displayed on the http://scores.epsn.go.com
        teamName={0: "Exit", 1:"Old Dominion", 2:"Florida", 3:"Virginia Tech", 4:"Penn St"}
        print "1. ",teamName[1]
        print "2. ",teamName[2]
        print "3. ",teamName[3]
        print "4. ",teamName[4]
        print "0. ",teamName[0]
        #raw_input() function reads a line from input (i.e. the user) and returns a string by stripping a trailing newline
        try:
            #convert the entered value to an integer to match the key of our associative array
            teamOption=int(raw_input("Select your favorite team" +" >> "))
            if teamOption >= 0 and teamOption <= 4:
                team=teamName[teamOption]
                if teamOption == 0:
                    sys.exit(0)
                else:
                    return team
            else:
                raise ValueError 
        except (ValueError):
            print ""
            print "Option must be a number between 0 and 4. Please try again."
            print ""
def scoreboardMenu(p_teamName):
    #Display the menu until user selects a valid option
    while True:
        #Set the baseURI. Add the parameters after user selects an option
        baseURI="http://scores.espn.go.com/ncf/scoreboard?confId=80&"
        #Associative array stores the menu options
        scoreboardOption={0:"Exit", 1:"2013 Season (Week 2)", 2:"2013 Season (Week 1)", 3:"2012 Season (Week 1)"}
        #These are the parameters which will be appended to the baseURI
        parameters={1:"seasonYear=2013&seasonType=2&weekNumber=2", 2:"seasonYear=2013&seasonType=2&weekNumber=1",3:"seasonYear=2012&seasonType=2&weekNumber=1"}
        print "1. ",scoreboardOption[1]
        print "2. ",scoreboardOption[2]
        print "3. ",scoreboardOption[3]
        print "0. ",scoreboardOption[0]
        try:
            #convert the entered value to an integer to match the keys of parameters list
            scoreboardOption=int(raw_input("Choose the matchup for " + p_teamName+" >> "))
            if scoreboardOption >= 0 and scoreboardOption <= 3:
                fullURI=baseURI+parameters[scoreboardOption]
                if scoreboardOption == 0:
                    sys.exit(0)
                else:
                    return fullURI
            else:
                raise ValueError
        except (ValueError):
             print ""
             print "Option must be a number between 0 and 3. Please try again."
             print ""
def sleepMenu():
    #Display the menu until user selects a valid option
    while True:
        try:
            #convert the entered value to an integer
            sleepOption=int(raw_input("Check for score updates. Enter frequency in seconds" + " >> "))
            if sleepOption > 0:
                return sleepOption
            else:
                raise ValueError
        except (ValueError):
             print ""
             print "Update frequency must be a number greater than 0. Please try again."
             print ""             
############################################################################             
#  This is main procedure in this package
############################################################################
def scoreCenter():
    #Print the team selection menu
    team=teamSelectionMenu()
    #Select the weekly matchup 
    uri=scoreboardMenu(team)
    #Set the update frequency
    sleepSeconds=sleepMenu()

    print "Press Control-C to exit"
    #display updated score until Control-C is entered from keyboard
    while True:
        try:
            #package the request
            request=urllib2.Request(uri)
            request.add_header('User-agent','Mozilla 5.10')
            response=urllib2.urlopen(request)
            html=response.read()
            print "Last update: ", response.info()['date']
            soup=BeautifulSoup(html)
            soup=BeautifulSoup(soup.prettify())
            visitingTeamsRec={}
            gameNumber=1
            for visitingTeam in soup.html.body.findAll('div',{'class' : 'team visitor'}):
                #first anchor after the <div> is the name of the visiting team
                visitingTeamName=str(visitingTeam.find('a').get('title')).strip()
                #<li class="final" id="332412579-aTotal">20</li>
                visitingScore=visitingTeam.find('li', {'class' : 'final'}).string.strip()
                #create a parallel list for the visiting teams
                visitingTeamsRec[gameNumber] = visitingTeamName + " " + visitingScore
                gameNumber=gameNumber+1
                
            homeTeamsRec={}
            gameNumber=1
            for homeTeam in soup.html.body.findAll('div',{'class' : 'team home'}):
                #first anchor after the <div> is the name of the home team
                homeTeamName=str(homeTeam.find('a').get('title')).strip()
                #<li class="final" id="332412579-aTotal">20</li>
                homeScore=homeTeam.find('li', {'class' : 'final'}).string.strip()
                #create a parallel list for the home teams
                homeTeamsRec[gameNumber] = homeTeamName + " " + homeScore
                gameNumber=gameNumber+1

            #iterate through all the game scores until the selected team is found   
            gameNumber=1
            while gameNumber <= len(visitingTeamsRec):
                visitor=visitingTeamsRec[gameNumber].strip()
                home=homeTeamsRec[gameNumber].strip()
                if home.startswith(team) or visitor.startswith(team):
                    print home, visitor
                gameNumber=gameNumber+1
            time.sleep(sleepSeconds)
        #Raised when the user hits the interrupt key (normally Control-C or Delete).
        except KeyboardInterrupt:
            print ""
            print "scoreCenter updates terminated."
            sys.exit(0)
    response.close()
