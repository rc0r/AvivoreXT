#AvivoreXT

###The Twitter-searching Data Miner

Avivore is a Python-based tool that searches Twitter for keywords and then
parses any tweets that are found. A configuration file defines search terms and
regular expressions that are used to extract data.

With the sample configuration file Avivore looks for the following sort of data:

* Phone numbers in NPA-NXX format (ex: 604-555-1212)
* IPv4 addresses (127.0.0.1)
* Blackberry PINs (ABCDEF12)

Of course, more data sets can be defined in the configuration file.

It presently uses a SQLite backend to store the data that is found and outputs
results via a stdout.


###Requirements

* Python 2.7, 3
* SQLite3
* Twitter-Application-Only-Authentication-OAuth-Python  
(https://github.com/hlt99/Twitter-Application-Only-Authentication-OAuth-Python)


### Installation

Follow these installation steps:

1.	Clone AvivoreXT repository:  
  
		$ git clone https://github.com/hlt99/AvivoreXT

2.	Clone Twitter-App-Only-OAuth repository:  
  
		$ git clone https://github.com/hlt99/Twitter-Application-Only-Authentication-OAuth-Python

3.	Copy oauth.py into AvivoreXT directory:  
  
		$ cp Twitter-Application-Only-Authentication-OAuth-Python/oauth.py AvivoreXT/

4.	Install remaining dependencies as required!

Now you're almost good to go. Check the next section for configuration and
usage instructions.


### Configuration & Usage

First, an AvivoreXT configuration file needs to be created. Probably the easiest
way to do this is to make a copy from the provided sample configuration file.
Now, with the editor of your choice set configuration options `consumer_key`
and `consumer_secret` in section `twitter_auth`. Both values can be obtained
from https://dev.twitter.com/apps after registration of a new Twitter app.
Comments explain all remaining options in the config file. After defining data
sets and search terms as needed you're good to go. Both are located in sections
`twitter_search_objects` and `twitter_search` respectively.

Running AvivoreXT is quite easy:

	$ cp sample.conf avivore.conf
	# edit config file according to needs
	# start mining
	$ python ./avivore.py avivore.conf

Have fun!
