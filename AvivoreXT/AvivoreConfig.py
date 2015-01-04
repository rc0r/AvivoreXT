# -*- coding: utf8 -*-
from AvivoreXT import Compat, Helper
import os
import sqlite3 as lite

if Compat.is_python3():
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser

class AvivoreConfig:
    def __init__(self, config_type, config_filename):
        self.config_type = config_type
        self.config_filename = config_filename
        self.config = ConfigParser()
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
                except Exception:
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
                twitter_search_term = qresult[5].strip(" \n")
                twitter_search_terms_raw = twitter_search_term.split(',')
                for x in twitter_search_terms_raw:
                    self.twitter_search_terms.append(x)

                # read other settings
                self.database_path = qresult[0].strip()
                self.twitter_consumer_key = qresult[1].strip()
                self.twitter_consumer_secret = qresult[2].strip()
                self.credentials_file = qresult[3].strip()
                self.twitter_track_keywords = qresult[4].strip()
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
                Helper.output("Sorry, no valid configuration found in database!")
                Helper.output("Please update missing configuration settings in your database and try again!")
                Helper.output("Exitting.")
                return -1
        return 0

    def init_config_database(self, config_database_path):
        if not os.path.isfile(config_database_path):
            Helper.output("Creating a new configuration database.")
        # dbcon = lite.connect(config_database_path)
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
            Helper.output("Using existing database to store results.")
            dbcon = lite.connect(self.database_path)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT Count(*) FROM Data")
            Helper.output(str(dbcur.fetchone()[0]) + " entries in this database so far.")
            '''
            # Removed the items below due to a bug. It's not needed really.
            DBCur.execute("SELECT * FROM Data ORDER BY TimeRecv ASC LIMIT 1")
            print DBCur.fetchone()[0]
            DatabaseFirstWrite = float(DBCur.fetchone()[0]) + 2
            Output("Database first written to " + str(DataBaseFirstWrite))
            '''
        else:  # If the database doesn't exist, we'll create it.
            if status == 1:  # If we desire to save the database, it will output this message.
                Helper.output("Creating a new database to store data!")
                # Eventually I'll set this up to just delete the DB at close should it be chosen as an option.
            dbcon = lite.connect(self.database_path)
            dbcur = dbcon.cursor()
            dbcur.execute(
                "CREATE TABLE Data (TimeRecv int, Type int, User text, UserId text, Value text, TID int, Message text)")
