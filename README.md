#AvivoreXT

###The Twitter-searching Data Miner

AvivoreXT is a multi-threaded, Python-based tool that searches Twitter for keywords and then parses any tweets that are found. For maximum data coverage AvivoreXT uses a mix of issuing classic search queries to the Twitter API and monitoring the Twitter Sreaming API.  

A configuration file defines search terms and regular expressions that are used to extract data. It presently uses a SQLite back-end to store the data that is found and outputs results via stdout.

With the sample configuration file AvivoreXT looks for the following sort of data:

* Phone numbers in NPA-NXX format (ex: 604-555-1212)
* IPv4 addresses (127.0.0.1)
* Blackberry PINs (ABCDEF12)

**Of course, more data sets can be defined in the configuration file.**

AvivoreXT is based on Avivore originally developed by Colin Keigher
(https://github.com/ColinKeigher/Avivore).


###Requirements

* Python 2.7+
* SQLite3
* Python Twitter API (https://github.com/RouxRC/twitter)
* Twitter-Application-Only-Authentication-OAuth-Python  
(https://github.com/rc0r/Twitter-Application-Only-Authentication-OAuth-Python)

Optional:

* sqliteboy (https://github.com/nopri/sqliteboy) for SQLite web front-end


###Installation

Follow these installation steps:

1.	Clone AvivoreXT repository:  
  
		$ git clone https://github.com/rc0r/AvivoreXT

2.	Clone Twitter-App-Only-OAuth repository:  
  
		$ git clone https://github.com/rc0r/Twitter-Application-Only-Authentication-OAuth-Python

3.	Copy oauth.py into AvivoreXT directory:  
  
		$ cp Twitter-Application-Only-Authentication-OAuth-Python/oauth.py AvivoreXT/

4.	Install remaining dependencies as required!


Now you're almost good to go. Check the next section for configuration and
usage instructions.


###Configuration & Usage

First, an AvivoreXT configuration file needs to be created. Probably the easiest
way to do this is to make a copy from the provided sample configuration file.
Now, with the editor of your choice set configuration options `consumer_key`
and `consumer_secret` in section `twitter_auth`. Both values can be obtained
from https://dev.twitter.com/apps after registration of a new Twitter app.
Comments explain all remaining options in the config file. After defining data sets and search terms as needed you're good to go. Both are located in sections `twitter_search_objects` and `twitter_search` respectively. Tracking keywords that are used to monitor the Twitter Streaming API can be configured by setting the option `stream_tracking_keyword` which is also found in section `twitter_search`.

Running AvivoreXT is quite easy:

	$ cp sample.conf avivore.conf
	# edit config file according to needs
	# start mining
	$ python ./avivore.py avivore.conf
	
When AvivoreXT is executed for the first time you'll be redirected to your browser to authenticate AvivoreXT to your user account. This is necessary because access to the Twitter Streaming API requires user based authentication. After you approved AvivoreXT in your browser, a PIN number is displayed. Switch back to the terminal and enter it. This step has to be performed only once. The generated user tokens will be stored in the credentials file that was set in the configuration file (option `credentials_file` in section `twitter_auth`).


###Notes on a front-end

Since AvivoreXT uses a SQLite3 database there exist quite a few options to use some kind of graphical front-end for database management and inspection. Recently I have been using [sqliteboy](https://github.com/nopri/sqliteboy) (see screenshots below) as it is quite lean, provides a clean web interface and allows for remote database access.

If the need arises for special AvivoreXT-related features, it's conceivable to integrate a similar interface into AvivoreXT with some useful extensions. If you think there's such a feature or AvivoreXT should have an integrated front-end, just let me know. Ideas and feature requests are always welcome.


###Screenshots

AvivoreXT v1.2.1 back-end

![ScreenShot](https://raw.github.com/rc0r/AvivoreXT/master/scrots/AvivoreXT-Backend.png)

[sqliteboy](https://github.com/nopri/sqliteboy) featured web front-end

![ScreenShot](https://raw.github.com/rc0r/AvivoreXT/master/scrots/AvivoreXT-Webfront.png)
