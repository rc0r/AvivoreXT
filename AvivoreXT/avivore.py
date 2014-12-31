#!/usr/bin/env python
# -*- coding: utf8 -*-

from twitter import *
import time
import re
import sys
import os
import sqlite3 as lite
import ConfigParser
import threading

"""
Helper functions
"""

def is_sequence(arg):
    # check if arg is list, tuple, ...
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))


class AvivoreConfig:
    def __init__(self, config_type, config_filename):
        self.config_type = config_type
        self.config_filename = str(config_filename)
        self.config = ConfigParser.ConfigParser()
        self.twitter_search_types = []
        self.twitter_search_terms = []
        self.twitter_track_keywords = None
        self.twitter_consumer_key = None
        self.twitter_consumer_secret = None
        self.twitter_search_interval = 30
        self.credentials_file = None
        self.database_path = None

    def read_config(self):
        if 0 == self.config_type:
            # open config file
            self.config.read(self.config_filename)

            # read data set definitions
            exists = True
            i = 0
            while exists:
                try:
                    self.twitter_search_types.append(self.config.get('twitter_search_objects', str(i), 0).strip("'\""))
                    i += 1
                except:
                    exists = False

            # read search term definitions
            twitter_search_term = self.config.get('twitter_search', 'csv_search_term', 0).strip(" '\"\n")
            twitter_search_terms_raw = twitter_search_term.split(',')
            for x in twitter_search_terms_raw:
                self.twitter_search_terms.append(x)

            # read other settings
            self.twitter_consumer_key = self.config.get('twitter_auth', 'consumer_key', 0).strip("'\"")
            self.twitter_consumer_secret = self.config.get('twitter_auth', 'consumer_secret', 0).strip("'\"")
            self.database_path = self.config.get('database', 'dbpath', 0).strip("'\"")
            self.credentials_file = self.config.get('twitter_auth', 'credentials_file', 0).strip("'\"")
            self.twitter_search_interval = int(self.config.get('twitter_search', 'interval', 0).strip("'\""))
            self.twitter_track_keywords = self.config.get('twitter_search', 'stream_tracking_keyword', 0).strip(" '\"")
        elif 1 == self.config_type:
            failed = False
            # prepare config database if it does not exist
            dbcur = self.init_config_database(self.config_filename)
            # read config from database
            string = "SELECT * FROM config"
            dbcur.execute(string)
            qresult = dbcur.fetchone()
            if qresult is not None:  # We should only have to pull one.
                # read search term definitions
                twitter_search_term = qresult[5].strip(" '\"\n")
                twitter_search_terms_raw = twitter_search_term.split(',')
                for x in twitter_search_terms_raw:
                    self.twitter_search_terms.append(x)

                # read other settings
                self.database_path = qresult[0].strip("'\"")
                self.twitter_consumer_key = qresult[1].strip("'\"")
                self.twitter_consumer_secret = qresult[2].strip("'\"")
                self.credentials_file = qresult[3].strip("'\"")
                self.twitter_track_keywords = qresult[4].strip("'\"")
                self.twitter_search_interval = int(qresult[6])
            else:
                failed = True

            if not failed:
                # read data set definitions
                string = "SELECT * FROM typedefs"
                dbcur.execute(string)
                qresults = dbcur.fetchall()
                if qresults is None:
                    failed = True
                else:
                    for qresult in qresults:
                        self.twitter_search_types.append(str(qresult[1]).strip("'\""))

            if failed:
                Output("Sorry, no valid configuration found in database!")
                Output("Please update missing configuration settings in your database and try again!")
                Output("Exitting.")
                return -1
        return 0

    def init_config_database(self, config_database_path):
        if not os.path.isfile(config_database_path):
             Output("Creating a new configuration database.")
        #     dbcon = lite.connect(config_database_path)
        #     dbcur = dbcon.cursor()
        #     dbcur.execute("SELECT Count(*) FROM Config")
        #     Output(str(dbcur.fetchone()[0]) + " entries in table Config so far.")
        #     dbcur.execute("SELECT Count(*) FROM TypeDefs")
        #     Output(str(dbcur.fetchone()[0]) + " entries in table TypeDefs so far.")
        #     '''
        #     # Removed the items below due to a bug. It's not needed really.
        #     DBCur.execute("SELECT * FROM Data ORDER BY TimeRecv ASC LIMIT 1")
        #     print DBCur.fetchone()[0]
        #     DatabaseFirstWrite = float(DBCur.fetchone()[0]) + 2
        #     Output("Database first written to " + str(DataBaseFirstWrite))
        #     '''
        #else:   # If the database doesn't exist, we'll create it.
        dbcon = lite.connect(config_database_path)
        dbcur = dbcon.cursor()
        dbcur.execute(
            "CREATE TABLE IF NOT EXISTS Config (dbpath text, consumer_key text, consumer_secret text, \
            credentials_file text, stream_tracking_keyword text, csv_search_term, interval int)")
        dbcur.execute("CREATE TABLE IF NOT EXISTS TypeDefs (Id int, Regex text, Comment text)")
        return dbcur

    def init_database(self, status):
        if os.path.isfile(self.database_path):
            Output("Using existing database to store results.")
            dbcon = lite.connect(self.database_path)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT Count(*) FROM Data")
            Output(str(dbcur.fetchone()[0]) + " entries in this database so far.")
            '''
            # Removed the items below due to a bug. It's not needed really.
            DBCur.execute("SELECT * FROM Data ORDER BY TimeRecv ASC LIMIT 1")
            print DBCur.fetchone()[0]
            DatabaseFirstWrite = float(DBCur.fetchone()[0]) + 2
            Output("Database first written to " + str(DataBaseFirstWrite))
            '''
        else:   # If the database doesn't exist, we'll create it.
            if status == 1:     # If we desire to save the database, it will output this message.
                Output("Creating a new database to store data!")
                # Eventually I'll set this up to just delete the DB at close should it be chosen as an option.
            dbcon = lite.connect(self.database_path)
            dbcur = dbcon.cursor()
            dbcur.execute(
                "CREATE TABLE Data (TimeRecv int, Type int, User text, UserId text, Value text, TID int, Message text)")


class Avivore:
    def __init__(self, avivore_config):
        assert isinstance(avivore_config, AvivoreConfig)
        self.avivore_config = avivore_config
        self.twitter_stream_instance = None
        self.twitter_instance = None
        self.twitter_bearer_token = None

    """
    Twitter-related functions.
    """

    def twitter_auth(self):
        self.twitter_bearer_token = oauth2_dance(self.avivore_config.twitter_consumer_key,
                                                 self.avivore_config.twitter_consumer_secret)
        self.twitter_instance = Twitter(auth=OAuth2(bearer_token=self.twitter_bearer_token))
        return self.twitter_instance


    def twitter_stream_auth(self):
        my_twitter_creds = os.path.expanduser(self.avivore_config.credentials_file)
        if not os.path.exists(my_twitter_creds):
            oauth_dance("twatting_search_cli", self.avivore_config.twitter_consumer_key,
                        self.avivore_config.twitter_consumer_secret, my_twitter_creds)

        oauth_token, oauth_secret = read_token_file(my_twitter_creds)
        self.twitter_stream_instance = TwitterStream(auth=OAuth(oauth_token, oauth_secret,
                                                                self.avivore_config.twitter_consumer_key,
                                                                self.avivore_config.twitter_consumer_secret))
        return self.twitter_stream_instance

    """
    classic Twitter search query
    """

    def twitter_search(self, search_string):
        try:
#             search_results = search_for_a_tweet(self.twitter_bearer_token, search_string)
            search_results = self.twitter_instance.search.tweets(q=str(search_string))
            output = search_results['statuses']
        except:
            output = None   # If this bombs out, we have the option of at least spitting out a result.
            raise
        return output

    def twitter_read_tweet(self, string):
        i = -1
        for x in self.avivore_config.twitter_search_types:
            i += 1
            findtype = re.compile(x)
            result_raw = findtype.findall(string)
            if not result_raw:
                continue
            else:
                if is_sequence(result_raw[0]):
                    result = [x for x in result_raw[0] if x]
                else:
                    result = result_raw[0]

                if is_sequence(result):
                    result = result[0]

                return i, result
                # nothing found
        return -1, 0

    def process_tweet(self, string):
        # This is just to write the tweet to the DB and then to output it in a
        # friendly manner. I guess it can be cleaned up but it works.
        if self.__db_dup_check(string[3]) == 0:
            self.__db_write_value(time.time(), string[0], string[1], string[5],
                                  string[2], string[3], string[4])
            return "Type: " + str(string[0]) + ", User: " + string[1] + " (" + \
                   string[5] + "), Content: " + string[2] + ", TID: " + str(string[3])
        else:
            return 0

    def __db_dup_check(self, value):
        # The nice thing about using the SQL DB is that I can just have it make a query to make a duplicate check.
        # This can likely be done better but it's "good enough" for now.
        string = "SELECT * FROM Data WHERE TID IS \'" + str(int(value)) + "\'"
        con = lite.connect(self.avivore_config.database_path)
        cur = con.cursor()
        cur.execute(string)
        if cur.fetchone() is not None:  # We should only have to pull one.
            output = 1
        else:
            output = 0
        return output

    def __db_write_value(self, stime, stype, user, userid, value, tweetid, message):
        # Just a simple function to write the results to the database.
        con = lite.connect(self.avivore_config.database_path)
        qstring = "INSERT INTO Data VALUES(?, ?, ?, ?, ?, ?, ?)"
        with con:
            cur = con.cursor()
            cur.execute(qstring,
                        (unicode(stime), unicode(stype), unicode(user), unicode(userid),
                         unicode(value), unicode(tweetid), unicode(message)))
            #lid = cur.lastrowid


class QueryThread(threading.Thread):
    def __init__(self, avivore):
        self.avivore = avivore
        threading.Thread.__init__(self)

    def run(self):
        Output("Spawning query thread [Q].")
        twitter_query_main(self.avivore)


query_thread = None


def main(argv):
    # create AvivoreConfig instance
    if "-c" == argv[1]:
        config = AvivoreConfig(0, argv[2])
    elif "-d" == argv[1]:
        config = AvivoreConfig(1, argv[2])
    else:
        return -1

    # read & parse config file
    if 0 > config.read_config():
        return -1
    # prepare database
    config.init_database(0)

    # create Avivore instance
    avivore = Avivore(config)

    # spawn twitter search query thread
    global query_thread
    query_thread = QueryThread(avivore)
    query_thread.setDaemon(True)
    query_thread.start()

    # continue with twitter stream monitoring
    twitter_stream_main(avivore)

# performs classic search queries with configured time interval
def twitter_query_main(avivore):
    stored = []
    avivore.twitter_auth()
    while 1:
        for x in avivore.avivore_config.twitter_search_terms:
            twit_data = avivore.twitter_search(x)
            if twit_data is None:   # with defaults, it's unlikely that this
                                    # will come up
                message = "Nothing found for \"" + x + "\". Waiting " +\
                          str(avivore.avivore_config.twitter_search_interval) +\
                          " seconds..."
                Output("[Q] "+str(message))
            else:
                for y in avivore.twitter_search(x):
                    z = y['id'], y['created_at'], y['user']['screen_name'], y['text'], y['user']['id_str']
                    result = avivore.twitter_read_tweet(z[3])
                    if result[0] < 0:
                        pass
                    else:   # If something is found, then we'll process the tweet
                        stored = stored, int(z[0])
                        # result value, time, result itself, tweet ID, tweet itself, userId
                        string = result[0], z[2], str(result[1]), z[0], z[3], z[4]
                        message = avivore.process_tweet(string)
                        if 0 != message:
                            Output("[Q] " + str(message))
            time.sleep(avivore.avivore_config.twitter_search_interval)


# continuously checks twitter stream API
def twitter_stream_main(avivore):
    stored = []
    twitter_stream_inst = avivore.twitter_stream_auth()

    iterator = twitter_stream_inst.statuses.filter(track=avivore.avivore_config.twitter_track_keywords)

    for y in iterator:
        if 'id' in y and 'created_at' in y and 'user' in y and 'text' in y:
            # print y
            z = y['id'], y['created_at'], y['user']['screen_name'], y['text'], y['user']['id_str']
            result = avivore.twitter_read_tweet(z[3])
            if result[0] < 0:
                pass
            else:   # If something is found, then we'll process the tweet
                stored = stored, int(z[0])
                # result value, time, result itself, tweet ID, tweet itself, userId
                string = result[0], z[2], str(result[1]), z[0], z[3], z[4]
                message = avivore.process_tweet(string)
                if 0 != message:
                    Output("[S] " + str(message))


def Output(string):
    # Default text output for the console.
    if 0 == string:
        pass
    else:
        # This is sort of lame but whatever:
        print "[" + str(round(time.time(), 0))[:-2] + "]", string


def SoftwareInitMsg(version):
    print "AvivoreXT", version, "by rc0r (https://github.com/rc0r)"


def CheckUsage(argv):
    print_usage = False
    if 3 != len(argv):
        print_usage = True
    else:
        if argv[1] != "-c" and argv[1] != "-d":
            print_usage = True

    if print_usage:
        print "Usage: %s -c <config-file>|-d <config-dbfile>" % argv[0]
        sys.exit(-1)


def SoftwareExit(status, message):
    print ""
    print message
    sys.exit(status)


def start():
    SoftwareInitMsg("1.2.3.dev0")
    CheckUsage(sys.argv)
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        SoftwareExit(0, "Exiting the application.")
    except:
        main(sys.argv)
        raise

if __name__ == "__main__":
    start()
