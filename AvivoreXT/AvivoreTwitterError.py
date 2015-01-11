# -*- coding: utf8 -*-


class TwitterException(Exception):
    """
    Generic Twitter exception class
    """
    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, '%s' % msg)


class TwitterAuthenticationException(TwitterException):
    """
    Twitter exception class for authentication failures.
    """
    def __init__(self, reason):
        self.msg = 'Twitter authentication failure! Reason: %s' % (reason)
        TwitterException.__init__(self, self.msg)

