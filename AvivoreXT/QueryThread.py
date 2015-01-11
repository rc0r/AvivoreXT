# -*- coding: utf8 -*-
from AvivoreXT import Helper
import threading
import time


class QueryThread(threading.Thread):
    """
    Class implementing the thread that performs periodic twitter searches.
    """
    def __init__(self, avivore):
        self.avivore = avivore
        self.stored = []
        threading.Thread.__init__(self)

    def init_run(self):
        """
        Prints info message and performs application authentication with Twitter.

        :return:        None
        """
        Helper.output("Spawning query thread [Q].")
        self.avivore.twitter_auth()

    def run(self):
        """
        Contains threads main loop that runs until the user kills the AvivoreXT process or some serious error occurs.

        :return:        None
        """
        self.init_run()
        while 1:
            self.twitter_search(self.avivore)

    def extract_data_from_tweet(self, avivore, tweet):
        """
        Scans data for extractable data sets (previously defined in the 'TypeDefs' section of the AvivoreXT
        configuration) and if found stores them in the result database.

        :param avivore: Previously initialized Avivore instance.
        :param tweet:   The tweet to analyzed that was returned from Twitter as a JSON object.
        :return:        None
        """
        z = tweet['id'], tweet['created_at'], tweet['user']['screen_name'], tweet['text'], tweet['user']['id_str']
        result = avivore.twitter_read_tweet(z[3])
        if result[0] >= 0:  # If something is found, then we'll process the tweet
            self.stored = self.stored, int(z[0])
            # result value, time, result itself, tweet ID, tweet itself, userId
            string = result[0], z[2], result[1], z[0], z[3], z[4]
            message = avivore.process_tweet(string)
            if message is not None:
                Helper.output("[Q] " + message)

    def twitter_search(self, avivore):
        """
        Performs a Twitter search query for all keywords defined in 'csv_search_term' configuration option and returns
        all found tweets.

        :param avivore: Previously initialized Avivore instance.
        :return:        None
        """
        # performs classic search queries with configured time interval
        for x in avivore.avivore_config.twitter_search_terms:
                twit_data = avivore.twitter_search(x)
                if twit_data is not None:
                    for y in avivore.twitter_search(x):
                        self.extract_data_from_tweet(avivore, y)
                time.sleep(avivore.avivore_config.twitter_search_interval)
