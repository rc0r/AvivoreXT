# -*- coding: utf8 -*-

from AvivoreXT import Helper, AvivoreConfig
from twitter import *
from twitter.stream import Timeout, HeartbeatTimeout, Hangup
from urllib2 import URLError
import time
import re
import os
import sqlite3 as lite


class Avivore:
    def __init__(self, avivore_config):
        assert isinstance(avivore_config, AvivoreConfig.AvivoreConfig)
        self.avivore_config = avivore_config
        self.twitter_stream_instance = None
        self.twitter_instance = None
        self.twitter_bearer_token = None

    """
    Twitter-related functions.
    """

    def twitter_auth(self):
        try:
            self.twitter_bearer_token = oauth2_dance(self.avivore_config.twitter_consumer_key,
                                                     self.avivore_config.twitter_consumer_secret)
            self.twitter_instance = Twitter(auth=OAuth2(bearer_token=self.twitter_bearer_token))
        except (TwitterHTTPError, URLError):
            SystemExit(1, "[!] Can't authenticate, check your network connection!")
        except Exception as e:
            SystemExit(1, "[!] Unknown error:\n"+e)

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

    # continuously checks twitter stream API
    def twitter_stream_main(self):
        Helper.output("Beginning stream processing [S].")
        stored = []
        twitter_stream_inst = self.twitter_stream_auth()

        try:
            iterator = twitter_stream_inst.statuses.filter(track=self.avivore_config.twitter_track_keywords)

            for y in iterator:
                # tweet may be a delete or data msg
                if y is None:
                    pass
                # tweet may indicate a timeout
                elif y is Timeout:
                    Helper.output("[S] Stream timeout...")
                elif y is HeartbeatTimeout:
                    Helper.output("[S] Heartbeat timeout...")
                # tweet may indicate a hung up stream conn.
                elif y is Hangup:
                    Helper.output("[S] Stream hangup detected!")
                # ok, tweet seems to contain text, process it
                elif 'id' in y and 'created_at' in y and 'user' in y and 'text' in y:
                    # print y
                    z = y['id'], y['created_at'], y['user']['screen_name'], y['text'], y['user']['id_str']
                    result = self.twitter_read_tweet(z[3])
                    if result[0] < 0:
                        pass
                    else:  # If something is found, then we'll process the tweet
                        stored = stored, int(z[0])
                        # result value, time, result itself, tweet ID, tweet itself, userId
                        string = result[0], z[2], result[1], z[0], z[3], z[4]
                        message = self.process_tweet(string)
                        if 0 != message:
                            Helper.output("[S] " + message)
        except (TwitterHTTPError, URLError):
            Helper.output("[!] Can't connect to twitter stream! Check your network connection!")
        except Exception as e:
            Helper.output("[!] Unknown stream processing error:\n"+e)
        finally:
            Helper.output("[S] Stream processing stopped.")

    """
    classic Twitter search query
    """

    def twitter_search(self, search_string):
        try:
            search_results = self.twitter_instance.search.tweets(q=search_string)
            output = search_results['statuses']
        except (TwitterHTTPError, URLError):
            Helper.output("[!] Problem connecting to twitter...")
            output = None  # If this bombs out, we have the option of at least spitting out a result.
        except Exception as e:
            Helper.output("[!] Unknown problem querying twitter:\n"+e)
            output = None  # If this bombs out, we have the option of at least spitting out a result.
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
                if Helper.is_sequence(result_raw[0]):
                    result = [x for x in result_raw[0] if x]
                else:
                    result = result_raw[0]

                if Helper.is_sequence(result):
                    result = result[0]

                return i, result
                # nothing found
        return -1, 0

    def process_tweet(self, string):
        # This is just to write the tweet to the DB and then to output it in a
        # friendly manner. I guess it can be cleaned up but it works.
        if self.__db_dup_check(string[3], string[2]) == 0:
            self.__db_write_value(time.time(), string[0], string[1], string[5],
                                  string[2], string[3], string[4])
            return "Type: " + str(string[0]) + ", User: " + string[1] + " (" + \
                   string[5] + "), Content: " + string[2] + ", TID: " + str(string[3])
        else:
            return 0

    """
    Database related functions
    """

    def __db_dup_check(self, tid, value):
        # The nice thing about using the SQL DB is that I can just have it make
        # a query to make a duplicate check. This can likely be done better but
        # it's "good enough" for now.
        output = 0
        con = lite.connect(self.avivore_config.database_path)
        cur = con.cursor()

        if output == 0:
            # check TweetID (TID)
            string = "SELECT * FROM Data WHERE TID IS \'" + str(int(tid)) + "\'"
            cur.execute(string)
            if cur.fetchone() is not None:  # We should only have to pull one.
                output = 1

        if output == 0:
            # check extracted data value
            string = "SELECT * FROM Data WHERE Value IS \'" + value + "\'"
            cur.execute(string)
            if cur.fetchone() is not None:
                output = 1

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
            # lid = cur.lastrowid