# -*- coding: utf8 -*-
from AvivoreXT import Compat, Helper
import os
import sqlite3 as lite

if Compat.is_python3():
    from configparser import ConfigParser, NoOptionError, MissingSectionHeaderError
else:
    from ConfigParser import ConfigParser, NoOptionError, MissingSectionHeaderError


class AvivoreConfigException(Exception):
    """
    Generic AvivoreConfig exception class
    """
    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, '%s' % msg)


class MissingConfigItemException(AvivoreConfigException):
    """
    AvivoreConfig exception class for missing configuration items in an AvivoreXT configuration.
    """
    def __init__(self, section, option):
        self.msg = 'Mandatory config item \'%s\' missing in section \'%s\'!' % (option, section)
        AvivoreConfigException.__init__(self, self.msg)


class AvivoreConfig:
    """
    Class for storing and managing AvivoreXT configuration options.
    """
    def __init__(self, config_type, config_filename):
        if not Helper.is_string(config_filename):
            raise AvivoreConfigException('Invalid config file specified!')
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
        self.mandatory_options = [
            # Be sure to keep order of database table layout for options from 'config' database
            # append type definitions for twitter_search_objects!
            ('database', 'dbpath'),
            ('twitter_auth', 'consumer_key'),
            ('twitter_auth', 'consumer_secret'),
            ('twitter_auth', 'credentials_file'),
            ('twitter_search', 'stream_tracking_keyword'),
            ('twitter_search', 'csv_search_term'),
            ('twitter_search_objects', '0'),
        ]

    def has_mandatory_items(self):
        """
        Checks if mandatory config items (AvivoreConfig.mandatory_options) were read from a config file.

        :return:    Returns True, if all mandatory items were read from config file, False otherwise.
        """
        ret = True
        s = None
        for s in self.mandatory_options:
            if not self.config.has_option(s[0], s[1]):
                ret = False
                break
        return ret, s

    def read_config(self):
        """
        Reads configuration settings from a configuration file and stores configuration values in corresponding
        class member variables.

        :return:    None.
        """
        if 0 == self.config_type:
            try:
                # open config file
                if not os.path.isfile(self.config_filename):
                    raise AvivoreConfigException('Config file not found!')
                self.config.read(self.config_filename)
            except (MissingSectionHeaderError, UnicodeDecodeError):
                raise AvivoreConfigException('No valid config file specified!')

            # check config file for presence of mandatory items
            (has_all, config_item) = self.has_mandatory_items()
            if not has_all:
                raise MissingConfigItemException(config_item[0], config_item[1])

            # read data set definitions
            exists = True
            i = 0
            while exists:
                try:
                    self.twitter_search_types.append(self.config.get('twitter_search_objects', str(i), raw=True).strip('\'\"'))
                    i += 1
                except NoOptionError:
                    exists = False

            # read search term definitions
            twitter_search_term = self.config.get('twitter_search', 'csv_search_term', raw=True).strip(' \'\"\n')
            twitter_search_terms_raw = twitter_search_term.split(',')
            for x in twitter_search_terms_raw:
                self.twitter_search_terms.append(x)

            # read other settings
            self.twitter_consumer_key = self.config.get('twitter_auth', 'consumer_key', raw=True).strip('\'\"')
            self.twitter_consumer_secret = self.config.get('twitter_auth', 'consumer_secret', raw=True).strip('\'\"')
            self.database_path = self.config.get('database', 'dbpath', raw=True).strip('\'\"')
            self.credentials_file = self.config.get('twitter_auth', 'credentials_file', raw=True).strip('\'\"')
            self.twitter_search_interval = int(self.config.get('twitter_search', 'interval', raw=True).strip('\'\"'))
            self.twitter_track_keywords = self.config.get('twitter_search', 'stream_tracking_keyword', raw=True).strip(
                ' \'\"')
        elif 1 == self.config_type:
            # prepare config database if it does not exist
            dbcur = self.init_config_database(self.config_filename)
            # read config from database
            string = 'SELECT * FROM config'
            dbcur.execute(string)
            qresult = dbcur.fetchone()
            if qresult is not None:  # We should only have to pull one.
                # check if mandatory options are in 'config' database
                for q in range(0, 5, 1):
                    if qresult[q] is None or 0 == len(qresult[q]):
                        raise MissingConfigItemException('Database.config', self.mandatory_options[q][1])

                # read search term definitions
                twitter_search_term = qresult[5].strip(' \n')
                twitter_search_terms_raw = twitter_search_term.split(',')
                for x in twitter_search_terms_raw:
                    self.twitter_search_terms.append(x)

                # read other settings
                self.database_path = qresult[0].strip()
                self.twitter_consumer_key = qresult[1].strip()
                self.twitter_consumer_secret = qresult[2].strip()
                self.credentials_file = qresult[3].strip()
                self.twitter_track_keywords = qresult[4].strip()

                if qresult[6] is not None:
                    self.twitter_search_interval = int(qresult[6])
            else:
                raise AvivoreConfigException('No valid (empty) configuration found in database!')

            # read data set definitions
            string = 'SELECT * FROM typedefs'
            dbcur.execute(string)
            qresults = dbcur.fetchall()
            if qresults is None or 0 == len(qresults):
                raise AvivoreConfigException('No data set type definitions found in database!')
            else:
                for qresult in qresults:
                    #print(qresult)
                    self.twitter_search_types.append(str(qresult[1]).strip('\'\"'))
        else:
            raise AvivoreConfigException('Invalid config type specified!')

    def init_config_database(self, config_database_path):
        """
        Prepares a sqlite3 database for use as a configuration database. Creates a database with the specified
        filename and creates empty 'Config' and 'TypeDefs' database tables that are going to hold all configuration
        settings.

        :param config_database_path: Path to database file.
        :return:    Returns a cursor to the sqlite3 database connection that can be used for further database
                    operations.
        """
        if not os.path.isfile(config_database_path):
            if not Helper.filepath_exists(config_database_path):
                raise AvivoreConfigException('Invalid path to configuration database file specified!')
            Helper.output('[W] Configuration database file not found!')
            Helper.output('[W] Creating a new configuration database.')
            Helper.output('[W] Now please store your configuration in database file \'%s\', then try again!'
                          % config_database_path)
        dbcon = lite.connect(config_database_path)
        dbcur = dbcon.cursor()
        dbcur.execute(
            'CREATE TABLE IF NOT EXISTS Config (dbpath text, consumer_key text, consumer_secret text, \
            credentials_file text, stream_tracking_keyword text, csv_search_term, interval int)')
        dbcur.execute('CREATE TABLE IF NOT EXISTS TypeDefs (Id int, Regex text, Comment text)')
        return dbcur

    def init_database(self):
        """
        Prepares a sqlite3 database for data set storage. If the file specified in AvivoreConfig.database_path
        doesn't exist a new sqlite3 database with table 'Data' is created. Otherwise the existing database is used to
        store additional data sets.

        :return:    None
        """
        if not Helper.is_string(self.database_path):
            raise AvivoreConfigException('Invalid database path specified!')

        table_data_exists = False

        if os.path.isfile(self.database_path):
            Helper.output('Using existing database to store results.')
            try:
                dbcon = lite.connect(self.database_path)
                dbcur = dbcon.cursor()
                dbcur.execute('SELECT Count(*) FROM Data')
                Helper.output(str(dbcur.fetchone()[0]) + ' entries in this database so far.')
                table_data_exists = True
            except lite.OperationalError:
                Helper.output('[W] Table \'Data\' not found in database!')

        if not table_data_exists:  # If the database doesn't exist, we'll create it.
            Helper.output('Creating new table \'Data\' in database \'%s\' to store data!' % self.database_path)
            dbcon = lite.connect(self.database_path)
            dbcur = dbcon.cursor()
            dbcur.execute(
                'CREATE TABLE Data (TimeRecv int, Type int, User text, UserId text, Value text, TID int, Message text)')
