#!/usr/bin/env python
# -*- coding: utf8 -*-

import time
from oauth import *
import re
import sys
import os
import locale
import sqlite3 as lite
import ConfigParser

"""
Here are the various settings we'll want to use for the application.
"""
TwitterSearchTerms = []
TwitterSearchTypes = []
TwitterSearchInterval = 30 # You'll want to set this to ten seconds or higher.
BearerToken = None
ConsumerKey = None
ConsumerSecret = None
DBPath = None

"""
Helper functions
"""
# check if arg is list, tuple, ...
def is_sequence(arg):
	return (not hasattr(arg, "strip") and
		hasattr(arg, "__getitem__") or
		hasattr(arg, "__iter__"))

"""
Twitter-related functions.
"""
def TwitterAuth():
	BearerToken = get_bearer_token(ConsumerKey,ConsumerSecret) # generates a bearer token
	return BearerToken

def TwitterSearch(string):
    try:
          search_results = search_for_a_tweet(BearerToken, string) # does a very basic search
	  output = search_results['statuses']
    except:
        output = None # If this bombs out, we have the option of at least spitting out a result.
    return output

def TwitterReadTweet(string):
	i=-1
	for x in TwitterSearchTypes:
		i=i+1
		FindType = re.compile(x)
		result_raw = FindType.findall(string)
		if result_raw == []:
			continue
		else:
			if(is_sequence(result_raw[0])):
				result = [x for x in result_raw[0] if x]
			else:
				result = result_raw[0]

			if(is_sequence(result)):
				result = result[0]
				
			return i, result
	# nothing found
	return -1, 0

"""
Various functions for this application.
"""
def Main():
    LastAction = time.time() # Sets the initial time to start our scan. It's not used however.
    Stored = []
    global BearerToken
    BearerToken = TwitterAuth()
    while 1:
        for x in TwitterSearchTerms:
            TwitData = TwitterSearch(x)
            if TwitData is None: # With the defaults, it's unlikely that this message will come up.
                message = "Nothing found for \"" + x + "\". Waiting " + str(TwitterSearchInterval) + " seconds to try again."
                Output(message)
            else:
                for y in TwitterSearch(x):
                    z = y['id'], y['created_at'], y['user']['screen_name'], y['text'], y['user']['id_str']
                    result = TwitterReadTweet(z[3])
                    if result[0] < 0:
                        pass
                    else: # If something is found, then we'll process the tweet
                        Stored = Stored, int(z[0])
                        string = result[0], z[2], str(result[1]), z[0], z[3], z[4] # result value, time, result itself, tweet ID, tweet itself, userId
                        message = ProcessTweet(string)
                        Output(message)
            time.sleep(TwitterSearchInterval) # This will pause the script 

def ReadConfig(string):
	# Very quick and really dirty! >:-}
	# Feel free to do some clean up...
	global DBPath
	global TwitterSearchTypes
	global TwitterSearchInterval
	global TwitterSearchTerms
	global ConsumerKey
	global ConsumerSecret

	config = ConfigParser.ConfigParser()
	# open config file
	config.read(string)
	
	# read data set definitions
	exists=True
	i=0
	while(exists==True):
		try:
			TwitterSearchTypes.append( config.get('twitter_search_objects', str(i), 0).strip("'") )
			i = i+1
		except:
			exists=False
	
	# read search term definitions
	twitter_search_term = config.get('twitter_search', 'csv_search_term', 0)
	twitter_search_terms_raw = twitter_search_term.split( ',' )
	for x in twitter_search_terms_raw:
		TwitterSearchTerms.append( x.strip(" '\n") )

	# read other settings
	ConsumerKey = config.get('twitter_auth', 'consumer_key', 0)
	ConsumerSecret = config.get('twitter_auth', 'consumer_secret', 0)
	DBPath = config.get('database', 'dbpath', 0)
	TwitterSearchInterval = int(config.get('twitter_search', 'interval', 0))

def Output(string):
    # Default text output for the console.
    if string == 0:
        pass
    else:
        print "[" + str(round(time.time(),0))[:-2] + "]", string # This is sort of lame but whatever.

def ProcessTweet(string): 
    # This is just to write the tweet to the DB and then to output it in a friendly manner.
    # I guess it can be cleaned up but it works.
    if DBDupCheck(string[3]) == 0:
        DBWriteValue(time.time(), string[0], string[1], string[5], string[2], string[3], string[4])
	return "Type: " + str(string[0]) + ", User: " + string[1] + " (" + string[5] + "), Content: " + string[2] + \
               ", TID: " + str(string[3])
    else:
        return 0

def DBDupCheck(value):
    # The nice thing about using the SQL DB is that I can just have it make a query to make a duplicate check.
    # This can likely be done better but it's "good enough" for now.
    string = "SELECT * FROM Data WHERE TID IS \'" + str(int(value)) + "\'"
    con = lite.connect(DBPath)
    cur = con.cursor()
    cur.execute(string)
    if cur.fetchone() != None: # We should only have to pull one.
        output = 1
    else:
        output = 0
    return output

def DBWriteValue(Time, Type, User, UserId, Value, TweetID, Message):
    # Just a simple function to write the results to the database.
    con = lite.connect(DBPath)
    qstring = "INSERT INTO Data VALUES(?, ?, ?, ?, ?, ?, ?)"
    with con:
        cur = con.cursor()
        cur.execute(qstring, ( unicode(Time), unicode(Type), unicode(User), unicode(UserId), unicode(Value), unicode(TweetID), unicode(Message) ) )
        lid = cur.lastrowid

def InitDatabase(status, filename):
    if os.path.isfile(filename):
        Output("Using existing database to store results.")
        DBCon = lite.connect(filename)
        DBCur = DBCon.cursor()
        DBCur.execute("SELECT Count(*) FROM Data")
        Output(str(DBCur.fetchone()[0]) + " entries in this database so far.")
	'''
        # Removed the items below due to a bug. It's not needed really.
        DBCur.execute("SELECT * FROM Data ORDER BY TimeRecv ASC LIMIT 1")
        print DBCur.fetchone()[0]
        DatabaseFirstWrite = float(DBCur.fetchone()[0]) + 2
        Output("Database first written to " + str(DataBaseFirstWrite))
        '''
    else: # If the database doesn't exist, we'll create it.
        if status == 1: # If we desire to save the database, it will output this message.
            Output("Creating a new database to store data!")
        # Eventually I'll set this up to just delete the DB at close should it be chosen as an option.
        DBCon = lite.connect(filename)
        DBCur = DBCon.cursor()
        DBCur.execute("CREATE TABLE Data (TimeRecv int, Type int, User text, UserId text, Value text, TID int, Message text)")

def SoftwareInitMsg(version):
    print "AvivoreXT", version, "by rc0r (https://github.com/rc0r)"

def CheckUsage(argv):
	if(len(argv)!=2):
		print "Usage: %s <config-file>" % argv[0]
		sys.exit(-1)

def SoftwareExit(type, message):
    print ""
    print message

"""
Here we go!
"""
if __name__ == "__main__":
    SoftwareInitMsg("1.1.1")
    CheckUsage(sys.argv)
    ReadConfig(sys.argv[1])
    InitDatabase(0, DBPath)
    try:
        Main()
    except KeyboardInterrupt:
        SoftwareExit(0, "Exiting the application.")
    except:
        Main()
        raise
