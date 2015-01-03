# -*- coding: utf8 -*-
from AvivoreXT import Avivore, Helper
import threading
import time


class QueryThread(threading.Thread):
    def __init__(self, avivore):
        self.avivore = avivore
        threading.Thread.__init__(self)

    def run(self):
        Helper.output("Spawning query thread [Q].")
        self.twitter_query_main(self.avivore)

    # performs classic search queries with configured time interval
    def twitter_query_main(self, avivore):
        stored = []
        avivore.twitter_auth()
        while 1:
            for x in avivore.avivore_config.twitter_search_terms:
                twit_data = avivore.twitter_search(x)
                if twit_data is not None:
                    for y in avivore.twitter_search(x):
                        z = y['id'], y['created_at'], y['user']['screen_name'], y['text'], y['user']['id_str']
                        result = avivore.twitter_read_tweet(z[3])
                        if result[0] < 0:
                            pass
                        else:  # If something is found, then we'll process the tweet
                            stored = stored, int(z[0])
                            # result value, time, result itself, tweet ID, tweet itself, userId
                            string = result[0], z[2], result[1], z[0], z[3], z[4]
                            message = avivore.process_tweet(string)
                            if 0 != message:
                                Helper.output("[Q] " + message)
                time.sleep(avivore.avivore_config.twitter_search_interval)
